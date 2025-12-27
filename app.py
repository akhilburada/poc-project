"""
Healthcare SLM Fine-tuning POC
Main Streamlit Application - Using Local Ollama Models

This application demonstrates:
1. File upload for healthcare datasets
2. Real-time "training" visualization (Modelfile approach)
3. Before/After comparison chatbot using Ollama
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
import os
import tempfile
from datetime import datetime

# Import our modules
from src.config import app_config
from src.data_processor import HealthcareDataProcessor, create_sample_healthcare_data
from src.ollama_client import (
    OllamaClient, 
    HealthcareOllamaTrainer, 
    check_ollama_status
)
from src.fine_tuner import TrainingMetrics

# Page configuration
st.set_page_config(
    page_title=app_config.page_title,
    page_icon=app_config.page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .ollama-status {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .ollama-running {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .ollama-stopped {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    .before-response {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    .after-response {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    .model-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        'training_metrics': [],
        'trainer': None,
        'is_trained': False,
        'training_data': None,
        'data_stats': None,
        'chat_history': [],
        'ollama_status': None,
        'selected_model': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header():
    """Render the main header"""
    st.markdown(
        '<div class="main-header">🏥 Healthcare SLM Fine-tuning POC</div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Using Local Ollama Models (Phi3, Llama 3.2)</div>', 
        unsafe_allow_html=True
    )


def render_ollama_status():
    """Check and display Ollama status"""
    status = check_ollama_status()
    st.session_state.ollama_status = status
    
    if status['running']:
        st.markdown(f"""
        <div class="ollama-status ollama-running">
            ✅ <strong>Ollama is running</strong><br>
            📦 Available models: {', '.join(status['models']) if status['models'] else 'None'}
        </div>
        """, unsafe_allow_html=True)
        
        if not status['models']:
            st.warning("⚠️ No models found. Please pull a model: `ollama pull phi3:mini`")
            return False
        return True
    else:
        st.markdown("""
        <div class="ollama-status ollama-stopped">
            ❌ <strong>Ollama is not running</strong><br>
            Please start Ollama: <code>ollama serve</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.error("""
        ### How to start Ollama:
        
        1. Open a terminal
        2. Run: `ollama serve`
        3. In another terminal, pull models:
           - `ollama pull phi3:mini`
           - `ollama pull llama3.2:1b`
        4. Refresh this page
        """)
        return False


def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Ollama Status
        st.subheader("🦙 Ollama Status")
        if st.button("🔄 Refresh Status"):
            st.session_state.ollama_status = check_ollama_status()
            st.rerun()
        
        status = st.session_state.ollama_status or check_ollama_status()
        
        if status['running']:
            st.success("✅ Ollama Running")
            
            # Model Selection
            st.subheader("🤖 Model Selection")
            
            if status['models']:
                # Prioritize recommended models
                recommended = status.get('recommended_models', [])
                all_models = status['models']
                
                # Sort to show recommended first
                sorted_models = sorted(all_models, key=lambda x: x not in recommended)
                
                selected_model = st.selectbox(
                    "Select Base Model",
                    sorted_models,
                    help="Choose phi3:mini or llama3.2:1b for best results"
                )
                st.session_state.selected_model = selected_model
                
                # Show model info
                st.info(f"📌 Selected: **{selected_model}**")
            else:
                st.warning("No models available")
                selected_model = None
        else:
            st.error("❌ Ollama Not Running")
            selected_model = None
        
        st.divider()
        
        # Training Configuration
        st.subheader("🎛️ Training Settings")
        
        training_speed = st.select_slider(
            "Training Speed",
            options=["Fast (Demo)", "Normal", "Thorough"],
            value="Fast (Demo)",
            help="Fast mode is optimized for live demos"
        )
        
        max_knowledge_items = st.slider(
            "Max Knowledge Items",
            min_value=10,
            max_value=100,
            value=50,
            help="Number of Q&A pairs to embed in model"
        )
        
        st.divider()
        
        # Session Info
        st.subheader("📊 Session Info")
        st.write(f"**Status**: {'✅ Trained' if st.session_state.is_trained else '⏳ Not Trained'}")
        if st.session_state.training_data:
            st.write(f"**Dataset**: {len(st.session_state.training_data)} samples")
        if st.session_state.trainer and st.session_state.trainer.trained_model_name:
            st.write(f"**Trained Model**: {st.session_state.trainer.trained_model_name}")
        
        return {
            'selected_model': selected_model,
            'training_speed': training_speed,
            'max_knowledge_items': max_knowledge_items,
        }


def render_data_upload():
    """Render the data upload section"""
    st.header("📁 Step 1: Upload Healthcare Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Upload your healthcare Q&A dataset. The model will learn from these question-answer pairs.
        
        **Supported formats:** CSV, JSON, JSONL, TXT
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a file (max 100MB)",
            type=['csv', 'json', 'jsonl', 'txt'],
            help="Upload healthcare Q&A data"
        )
        
        st.divider()
        
        use_sample = st.checkbox(
            "📝 Use sample healthcare dataset instead", 
            value=not uploaded_file
        )
        
    with col2:
        st.markdown("### 📋 Expected Format")
        st.code("""
// JSON format:
{
  "instruction": "What is diabetes?",
  "response": "Diabetes is..."
}

// CSV format:
question,answer
"What is diabetes?","Diabetes is..."
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
                    suffix = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    processed = processor.process_file(tmp_path)
                    conversations = processed.conversations
                    stats = processed.data_stats
                    
                    os.unlink(tmp_path)
            
            st.session_state.training_data = conversations
            st.session_state.data_stats = stats
            
            # Display stats
            st.success(f"✅ Data loaded! **{len(conversations)}** Q&A pairs ready for training.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Samples", stats['total_samples'])
            with col2:
                st.metric("Avg Question Length", f"{stats['avg_instruction_length']:.0f} chars")
            with col3:
                st.metric("Avg Answer Length", f"{stats['avg_response_length']:.0f} chars")
            
            # Preview data
            with st.expander("👀 Preview Training Data", expanded=False):
                for i, conv in enumerate(conversations[:5]):
                    st.markdown(f"**Sample {i+1}:**")
                    q = conv['instruction']
                    a = conv['response']
                    st.markdown(f"*Q: {q[:200]}{'...' if len(q) > 200 else ''}*")
                    st.markdown(f"A: {a[:300]}{'...' if len(a) > 300 else ''}")
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
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(30, 136, 229, 0.1)'
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
        title_text="📈 Real-time Training Metrics"
    )
    
    fig.update_xaxes(title_text="Training Step", row=1, col=1)
    fig.update_yaxes(title_text="Loss", row=1, col=1)
    fig.update_xaxes(title_text="Training Step", row=1, col=2)
    fig.update_yaxes(title_text="Learning Rate", row=1, col=2)
    
    return fig


def render_training_section(config: dict):
    """Render the training section"""
    st.header("🚀 Step 2: Train the Model")
    
    if not st.session_state.training_data:
        st.warning("⚠️ Please upload or select training data first.")
        return False
    
    if not config['selected_model']:
        st.warning("⚠️ Please select a model in the sidebar.")
        return False
    
    # Training configuration display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ### Training Configuration
        
        | Setting | Value |
        |---------|-------|
        | **Base Model** | `{config['selected_model']}` |
        | **Training Data** | {len(st.session_state.training_data)} samples |
        | **Knowledge Items** | {min(config['max_knowledge_items'], len(st.session_state.training_data))} |
        | **Speed Mode** | {config['training_speed']} |
        
        **What happens during training:**
        1. Healthcare Q&A pairs are processed
        2. Knowledge is embedded into the model
        3. A specialized healthcare assistant is created
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
                # Cleanup old model
                if st.session_state.trainer:
                    st.session_state.trainer.cleanup()
                st.session_state.is_trained = False
                st.session_state.training_metrics = []
                st.session_state.trainer = None
                st.session_state.chat_history = []
                st.rerun()
    
    # Training execution
    if start_training:
        st.session_state.training_metrics = []
        
        # Create placeholders for real-time updates
        progress_bar = st.progress(0)
        status_text = st.empty()
        metrics_chart = st.empty()
        
        # Initialize trainer
        trainer = HealthcareOllamaTrainer(base_model=config['selected_model'])
        
        # Metrics collection
        collected_metrics = []
        
        def update_metrics(metrics: TrainingMetrics):
            collected_metrics.append(metrics)
            st.session_state.training_metrics = collected_metrics
            
            # Update chart
            if len(collected_metrics) > 1:
                fig = create_training_chart(collected_metrics)
                if fig:
                    metrics_chart.plotly_chart(fig, use_container_width=True)
            
            # Update progress
            progress = min(95, len(collected_metrics) * 5)
            progress_bar.progress(progress)
        
        def update_progress(message: str):
            status_text.info(f"🔄 {message}")
        
        try:
            start_time = time.time()
            
            # Limit data for training
            training_data = st.session_state.training_data[:config['max_knowledge_items']]
            
            # Generate unique model name
            model_name = f"healthcare-assistant-{int(time.time())}"
            
            # Train the model
            success = trainer.train(
                healthcare_data=training_data,
                model_name=model_name,
                progress_callback=update_progress,
                metrics_callback=update_metrics
            )
            
            elapsed_time = time.time() - start_time
            
            if success:
                st.session_state.trainer = trainer
                st.session_state.is_trained = True
                
                progress_bar.progress(100)
                status_text.success(f"✅ Training completed in {elapsed_time:.1f} seconds!")
                
                # Final chart
                if st.session_state.training_metrics:
                    fig = create_training_chart(st.session_state.training_metrics)
                    if fig:
                        metrics_chart.plotly_chart(fig, use_container_width=True)
                
                # Final metrics
                if st.session_state.training_metrics:
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
            else:
                st.error("Training failed. Please check Ollama status.")
                return False
                
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return False
    
    # Show existing training results
    elif st.session_state.is_trained and st.session_state.training_metrics:
        st.success("✅ Model is trained and ready!")
        fig = create_training_chart(st.session_state.training_metrics)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        if st.session_state.trainer:
            st.info(f"📦 Trained Model: `{st.session_state.trainer.trained_model_name}`")
    
    return st.session_state.is_trained


def render_chatbot_section(config: dict):
    """Render the chatbot comparison section"""
    st.header("💬 Step 3: Compare Before vs After")
    
    if not st.session_state.is_trained:
        st.warning("⚠️ Please complete model training first.")
        return
    
    if not st.session_state.trainer:
        st.error("Trainer not available. Please retrain.")
        return
    
    st.markdown("""
    Ask healthcare questions and compare responses:
    - **Before Training**: Base model without healthcare knowledge
    - **After Training**: Model with embedded healthcare knowledge
    """)
    
    # Sample questions
    st.markdown("### 💡 Try these sample questions:")
    
    sample_questions = [
        "What are the symptoms of diabetes?",
        "How do I schedule a doctor appointment?",
        "What is covered under preventive care?",
        "What should I do in a medical emergency?",
        "How can I manage high blood pressure?"
    ]
    
    cols = st.columns(len(sample_questions))
    selected_sample = None
    
    for i, (col, q) in enumerate(zip(cols, sample_questions)):
        with col:
            if st.button(f"Q{i+1}", help=q, use_container_width=True):
                selected_sample = q
    
    # Input field
    user_input = st.text_input(
        "Or type your own healthcare question:",
        value=selected_sample if selected_sample else "",
        placeholder="Type your question here..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_btn = st.button(
            "🔄 Generate & Compare", 
            type="primary", 
            use_container_width=True,
            disabled=not user_input
        )
    
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Generate responses
    if generate_btn and user_input:
        with st.spinner("Generating responses... (this may take a moment)"):
            try:
                # Generate BEFORE response (base model)
                before_response = st.session_state.trainer.generate_before(user_input)
                
                # Generate AFTER response (trained model)
                after_response = st.session_state.trainer.generate_after(user_input)
                
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
            idx = len(st.session_state.chat_history) - i
            
            with st.container():
                st.markdown(f"### Question {idx}")
                st.markdown(f"**🙋 {chat['question']}**")
                st.caption(f"Generated at {chat['timestamp']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ❌ Before Training")
                    st.markdown(f"*Base model: {config['selected_model']}*")
                    st.markdown(f"""
                    <div class="before-response">
                    {chat['before']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### ✅ After Training")
                    st.markdown(f"*Trained model: {st.session_state.trainer.trained_model_name}*")
                    st.markdown(f"""
                    <div class="after-response">
                    {chat['after']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()


def render_info_section():
    """Render additional information"""
    with st.expander("ℹ️ About This POC", expanded=False):
        st.markdown("""
        ### Healthcare SLM Fine-tuning POC
        
        This POC demonstrates customizing local Ollama models for healthcare domains.
        
        **How it works:**
        1. **Upload Data**: Healthcare Q&A pairs are loaded
        2. **Training**: Knowledge is embedded into the model via Modelfile
        3. **Comparison**: Before/After responses show the improvement
        
        **Technical Details:**
        - Uses local Ollama installation
        - Supports Phi3, Llama 3.2, and other models
        - Knowledge embedding via system prompts
        - No GPU required - runs on CPU
        
        **Note:** This POC uses the Modelfile approach for fast demos. 
        For true fine-tuning, additional tools like llama.cpp or Unsloth would be needed.
        """)
    
    with st.expander("🛠️ Troubleshooting", expanded=False):
        st.markdown("""
        ### Common Issues
        
        **Ollama not running:**
        ```bash
        ollama serve
        ```
        
        **No models available:**
        ```bash
        ollama pull phi3:mini
        ollama pull llama3.2:1b
        ```
        
        **Slow responses:**
        - First query loads the model (takes longer)
        - Subsequent queries are faster
        - Smaller models (phi3:mini) are faster than larger ones
        
        **Out of memory:**
        - Close other applications
        - Use smaller model (phi3:mini vs llama3.2)
        """)


def main():
    """Main application entry point"""
    initialize_session_state()
    
    render_header()
    
    # Check Ollama status first
    ollama_ok = render_ollama_status()
    
    if not ollama_ok:
        st.stop()
    
    config = render_sidebar()
    
    st.divider()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📁 Data Upload", "🚀 Training", "💬 Chatbot"])
    
    with tab1:
        data_ready = render_data_upload()
    
    with tab2:
        if data_ready:
            render_training_section(config)
        else:
            st.info("👆 Please upload training data in the 'Data Upload' tab first.")
    
    with tab3:
        render_chatbot_section(config)
    
    st.divider()
    render_info_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Healthcare SLM POC | Powered by Ollama + Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
