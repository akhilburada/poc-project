"""
Healthcare SLM Fine-tuning POC
Main Streamlit Application

This application demonstrates:
1. File upload for healthcare datasets
2. Real-time fine-tuning visualization
3. Before/After comparison chatbot
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
import os
import tempfile
import json
from datetime import datetime

# Import our modules
from src.config import app_config, model_config
from src.data_processor import HealthcareDataProcessor, create_sample_healthcare_data
from src.fine_tuner import HealthcareSLMFineTuner, BaselineModel, TrainingMetrics

# Page configuration
st.set_page_config(
    page_title=app_config.page_title,
    page_icon=app_config.page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .comparison-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .before-response {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .after-response {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'training_metrics' not in st.session_state:
        st.session_state.training_metrics = []
    if 'fine_tuner' not in st.session_state:
        st.session_state.fine_tuner = None
    if 'baseline_model' not in st.session_state:
        st.session_state.baseline_model = None
    if 'is_trained' not in st.session_state:
        st.session_state.is_trained = False
    if 'training_data' not in st.session_state:
        st.session_state.training_data = None
    if 'data_stats' not in st.session_state:
        st.session_state.data_stats = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">🏥 Healthcare SLM Fine-tuning POC</div>', 
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">CPU-based Small Language Model Training for Healthcare Domain</div>', 
        unsafe_allow_html=True
    )
    
    # Info boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📁 **Step 1**: Upload your healthcare dataset")
    with col2:
        st.info("🚀 **Step 2**: Fine-tune the model (< 5 min)")
    with col3:
        st.info("💬 **Step 3**: Compare before/after responses")


def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Model Settings")
        model_name = st.selectbox(
            "Base Model",
            ["distilgpt2", "gpt2", "facebook/opt-125m"],
            help="Select the base model for fine-tuning"
        )
        
        st.subheader("Training Parameters")
        num_epochs = st.slider("Number of Epochs", 1, 5, 2, 
                               help="More epochs = better learning but longer training")
        batch_size = st.slider("Batch Size", 1, 8, 4,
                               help="Larger batch = faster but more memory")
        learning_rate = st.select_slider(
            "Learning Rate",
            options=[1e-5, 2e-5, 5e-5, 1e-4, 2e-4],
            value=5e-5,
            format_func=lambda x: f"{x:.0e}"
        )
        max_steps = st.number_input(
            "Max Training Steps (0 = auto)",
            min_value=0,
            max_value=500,
            value=100,
            help="Limit steps for faster POC demo"
        )
        
        st.subheader("LoRA Settings")
        use_lora = st.checkbox("Use LoRA", value=True,
                               help="LoRA enables efficient fine-tuning with fewer parameters")
        
        st.divider()
        
        st.subheader("📊 Session Info")
        st.write(f"**Training Status**: {'✅ Trained' if st.session_state.is_trained else '⏳ Not Trained'}")
        if st.session_state.training_data:
            st.write(f"**Dataset Size**: {len(st.session_state.training_data)} samples")
        
        return {
            'model_name': model_name,
            'num_epochs': num_epochs,
            'batch_size': batch_size,
            'learning_rate': learning_rate,
            'max_steps': max_steps if max_steps > 0 else -1,
            'use_lora': use_lora
        }


def render_data_upload():
    """Render the data upload section"""
    st.header("📁 Step 1: Upload Healthcare Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Upload your healthcare Q&A dataset. Supported formats:
        - **CSV**: Columns for questions and answers
        - **JSON/JSONL**: Array of objects with instruction/response fields
        - **TXT**: Plain text with Q&A format
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'json', 'jsonl', 'txt'],
            help="Maximum file size: 100MB"
        )
        
        st.divider()
        
        use_sample = st.checkbox("📝 Use sample healthcare dataset instead", 
                                 value=not uploaded_file)
        
    with col2:
        st.markdown("### Expected Format")
        st.code("""
{
  "instruction": "What are diabetes symptoms?",
  "response": "Common symptoms include..."
}
        """, language="json")
    
    # Process data
    if uploaded_file or use_sample:
        processor = HealthcareDataProcessor(max_samples=app_config.max_training_samples)
        
        try:
            if use_sample:
                with st.spinner("Loading sample healthcare data..."):
                    conversations = create_sample_healthcare_data()
                    stats = {
                        'total_samples': len(conversations),
                        'avg_instruction_length': sum(len(c['instruction']) for c in conversations) / len(conversations),
                        'avg_response_length': sum(len(c['response']) for c in conversations) / len(conversations),
                    }
            else:
                with st.spinner("Processing uploaded file..."):
                    # Save to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    processed = processor.process_file(tmp_path)
                    conversations = processed.conversations
                    stats = processed.data_stats
                    
                    os.unlink(tmp_path)
            
            st.session_state.training_data = conversations
            st.session_state.data_stats = stats
            
            # Display stats
            st.success(f"✅ Data loaded successfully! {len(conversations)} samples ready for training.")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Samples", stats['total_samples'])
            with col2:
                st.metric("Avg Question Length", f"{stats['avg_instruction_length']:.0f} chars")
            with col3:
                st.metric("Avg Answer Length", f"{stats['avg_response_length']:.0f} chars")
            with col4:
                est_time = min(300, len(conversations) * 0.5)  # Rough estimate
                st.metric("Est. Training Time", f"{est_time:.0f}s")
            
            # Preview data
            with st.expander("👀 Preview Training Data", expanded=False):
                for i, conv in enumerate(conversations[:5]):
                    st.markdown(f"**Sample {i+1}:**")
                    st.markdown(f"*Q: {conv['instruction'][:200]}...*" if len(conv['instruction']) > 200 else f"*Q: {conv['instruction']}*")
                    st.markdown(f"A: {conv['response'][:300]}..." if len(conv['response']) > 300 else f"A: {conv['response']}")
                    st.divider()
                    
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            return False
    
    return st.session_state.training_data is not None


def create_training_chart(metrics: list):
    """Create real-time training visualization"""
    if not metrics:
        return None
    
    df = pd.DataFrame([
        {'step': m.step, 'loss': m.loss, 'lr': m.learning_rate, 'time': m.timestamp}
        for m in metrics
    ])
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Training Loss', 'Learning Rate Schedule')
    )
    
    # Loss curve
    fig.add_trace(
        go.Scatter(
            x=df['step'], 
            y=df['loss'],
            mode='lines+markers',
            name='Loss',
            line=dict(color='#1E88E5', width=2),
            marker=dict(size=6)
        ),
        row=1, col=1
    )
    
    # Learning rate
    fig.add_trace(
        go.Scatter(
            x=df['step'],
            y=df['lr'],
            mode='lines',
            name='Learning Rate',
            line=dict(color='#43A047', width=2)
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=350,
        showlegend=True,
        title_text="Real-time Training Metrics"
    )
    
    fig.update_xaxes(title_text="Training Step", row=1, col=1)
    fig.update_yaxes(title_text="Loss", row=1, col=1)
    fig.update_xaxes(title_text="Training Step", row=1, col=2)
    fig.update_yaxes(title_text="Learning Rate", row=1, col=2)
    
    return fig


def render_training_section(config: dict):
    """Render the training section"""
    st.header("🚀 Step 2: Fine-tune the Model")
    
    if not st.session_state.training_data:
        st.warning("⚠️ Please upload or select training data first.")
        return False
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        **Training Configuration:**
        - Model: `{config['model_name']}`
        - Epochs: {config['num_epochs']}
        - Batch Size: {config['batch_size']}
        - Learning Rate: {config['learning_rate']:.0e}
        - LoRA: {'Enabled ✓' if config['use_lora'] else 'Disabled'}
        - Max Steps: {config['max_steps'] if config['max_steps'] > 0 else 'Auto'}
        """)
    
    with col2:
        start_training = st.button(
            "▶️ Start Training",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.is_trained
        )
        
        if st.session_state.is_trained:
            if st.button("🔄 Reset & Retrain", use_container_width=True):
                st.session_state.is_trained = False
                st.session_state.training_metrics = []
                st.session_state.fine_tuner = None
                st.rerun()
    
    # Training progress section
    if start_training:
        st.session_state.training_metrics = []
        
        # Create placeholders for real-time updates
        progress_bar = st.progress(0)
        status_text = st.empty()
        metrics_chart = st.empty()
        metrics_display = st.empty()
        
        # Initialize fine-tuner
        fine_tuner = HealthcareSLMFineTuner(
            model_name=config['model_name'],
            output_dir=app_config.model_output_dir,
            use_lora=config['use_lora']
        )
        
        def update_metrics(metrics: TrainingMetrics):
            """Callback to update metrics in real-time"""
            st.session_state.training_metrics.append(metrics)
            fine_tuner.training_history.append(metrics)
        
        def update_progress(message: str):
            """Callback to update progress"""
            status_text.info(f"🔄 {message}")
        
        try:
            start_time = time.time()
            
            # Train the model
            result = fine_tuner.train(
                conversations=st.session_state.training_data,
                num_epochs=config['num_epochs'],
                batch_size=config['batch_size'],
                learning_rate=config['learning_rate'],
                max_steps=config['max_steps'],
                metrics_callback=update_metrics,
                progress_callback=update_progress
            )
            
            elapsed_time = time.time() - start_time
            
            # Store the fine-tuner
            st.session_state.fine_tuner = fine_tuner
            st.session_state.is_trained = True
            
            # Update final status
            progress_bar.progress(100)
            status_text.success(f"✅ Training completed in {elapsed_time:.1f} seconds!")
            
            # Display final chart
            if st.session_state.training_metrics:
                fig = create_training_chart(st.session_state.training_metrics)
                if fig:
                    metrics_chart.plotly_chart(fig, use_container_width=True)
                
                # Final metrics
                final_loss = st.session_state.training_metrics[-1].loss
                initial_loss = st.session_state.training_metrics[0].loss
                improvement = ((initial_loss - final_loss) / initial_loss) * 100
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Initial Loss", f"{initial_loss:.4f}")
                with col2:
                    st.metric("Final Loss", f"{final_loss:.4f}")
                with col3:
                    st.metric("Improvement", f"{improvement:.1f}%")
                with col4:
                    st.metric("Training Time", f"{elapsed_time:.1f}s")
            
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return False
    
    # Show training history if already trained
    elif st.session_state.is_trained and st.session_state.training_metrics:
        st.success("✅ Model is trained and ready!")
        fig = create_training_chart(st.session_state.training_metrics)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    return st.session_state.is_trained


def render_chatbot_section():
    """Render the chatbot comparison section"""
    st.header("💬 Step 3: Chat & Compare Responses")
    
    if not st.session_state.is_trained:
        st.warning("⚠️ Please complete model training first.")
        return
    
    st.markdown("""
    Compare responses from the **base model** (before training) vs the **fine-tuned model** (after training).
    Ask healthcare-related questions to see the improvement!
    """)
    
    # Sample questions
    st.markdown("**💡 Try these sample questions:**")
    sample_questions = [
        "What are the symptoms of diabetes?",
        "How do I schedule a doctor appointment?",
        "What is covered under preventive care?",
        "How can I manage high blood pressure?",
        "What should I do in a medical emergency?"
    ]
    
    cols = st.columns(len(sample_questions))
    selected_sample = None
    for i, (col, q) in enumerate(zip(cols, sample_questions)):
        with col:
            if st.button(f"Q{i+1}", help=q, use_container_width=True):
                selected_sample = q
    
    # Input field
    user_input = st.text_input(
        "Ask a healthcare question:",
        value=selected_sample if selected_sample else "",
        placeholder="Type your question here..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        generate_btn = st.button("🔄 Generate Responses", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Clear History", use_container_width=True)
    
    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()
    
    if generate_btn and user_input:
        with st.spinner("Generating responses..."):
            # Initialize baseline model if needed
            if st.session_state.baseline_model is None:
                st.session_state.baseline_model = BaselineModel(
                    model_name=st.session_state.fine_tuner.model_name
                )
                st.session_state.baseline_model.load()
            
            # Generate responses
            try:
                before_response = st.session_state.baseline_model.generate(user_input)
                after_response = st.session_state.fine_tuner.generate_response(user_input)
                
                # Add to history
                st.session_state.chat_history.append({
                    'question': user_input,
                    'before': before_response,
                    'after': after_response,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.divider()
        st.subheader("📝 Comparison Results")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                st.markdown(f"### Question {len(st.session_state.chat_history) - i}")
                st.markdown(f"**🙋 {chat['question']}**")
                st.caption(f"Generated at {chat['timestamp']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ❌ Before Fine-tuning")
                    st.markdown(f"""
                    <div class="before-response">
                    {chat['before']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### ✅ After Fine-tuning")
                    st.markdown(f"""
                    <div class="after-response">
                    {chat['after']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()


def render_info_section():
    """Render additional information section"""
    with st.expander("ℹ️ About This POC", expanded=False):
        st.markdown("""
        ### Healthcare SLM Fine-tuning POC
        
        This proof-of-concept demonstrates fine-tuning a Small Language Model (SLM) on healthcare data 
        using CPU-only infrastructure.
        
        **Key Features:**
        - 📁 Upload custom healthcare datasets (CSV, JSON, TXT)
        - 🚀 Fine-tune using LoRA for efficiency
        - 📊 Real-time training visualization
        - 💬 Before/After response comparison
        
        **Technical Details:**
        - Base Model: DistilGPT2 (82M parameters)
        - Fine-tuning Method: LoRA (Low-Rank Adaptation)
        - Training Target: < 5 minutes on CPU
        - Memory Usage: < 4GB RAM
        
        **Why SLMs for Healthcare?**
        - 🔒 On-premise deployment (data privacy)
        - 💰 Lower infrastructure costs
        - ⚡ Faster inference times
        - 🎯 Domain-specific optimization
        """)


def main():
    """Main application entry point"""
    initialize_session_state()
    
    render_header()
    config = render_sidebar()
    
    st.divider()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📁 Data Upload", "🚀 Training", "💬 Chatbot"])
    
    with tab1:
        data_ready = render_data_upload()
    
    with tab2:
        if data_ready:
            render_training_section(config)
        else:
            st.info("👆 Please upload or select training data in the 'Data Upload' tab first.")
    
    with tab3:
        render_chatbot_section()
    
    st.divider()
    render_info_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Healthcare SLM POC | Built with Streamlit & Hugging Face Transformers"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
