"""
Data processing utilities for healthcare datasets
"""
import os
import json
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class ProcessedData:
    """Container for processed training data"""
    conversations: List[Dict[str, str]]
    total_samples: int
    data_stats: Dict


class HealthcareDataProcessor:
    """Process various file formats into training-ready data"""
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.supported_formats = {
            '.txt': self._process_txt,
            '.csv': self._process_csv,
            '.json': self._process_json,
            '.jsonl': self._process_jsonl,
        }
    
    def process_file(self, file_path: str) -> ProcessedData:
        """Process a file and return training data"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {ext}")
        
        conversations = self.supported_formats[ext](file_path)
        
        # Limit samples for POC
        if len(conversations) > self.max_samples:
            conversations = conversations[:self.max_samples]
        
        stats = self._compute_stats(conversations)
        
        return ProcessedData(
            conversations=conversations,
            total_samples=len(conversations),
            data_stats=stats
        )
    
    def _process_txt(self, file_path: str) -> List[Dict[str, str]]:
        """Process plain text file - assumes Q&A format or paragraph format"""
        conversations = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to detect Q&A pattern
        qa_pattern = r'(?:Q:|Question:|User:)\s*(.*?)\s*(?:A:|Answer:|Assistant:|Bot:)\s*(.*?)(?=(?:Q:|Question:|User:)|$)'
        matches = re.findall(qa_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if matches:
            for question, answer in matches:
                conversations.append({
                    'instruction': question.strip(),
                    'response': answer.strip()
                })
        else:
            # Split into paragraphs and create instruction-response pairs
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            for i in range(0, len(paragraphs) - 1, 2):
                conversations.append({
                    'instruction': f"Explain: {paragraphs[i][:100]}...",
                    'response': paragraphs[i] + (f" {paragraphs[i+1]}" if i+1 < len(paragraphs) else "")
                })
        
        return conversations
    
    def _process_csv(self, file_path: str) -> List[Dict[str, str]]:
        """Process CSV file with question/answer columns"""
        df = pd.read_csv(file_path)
        conversations = []
        
        # Try to identify instruction and response columns
        instruction_cols = ['question', 'query', 'input', 'instruction', 'prompt', 'user', 'text']
        response_cols = ['answer', 'response', 'output', 'assistant', 'reply', 'label']
        
        inst_col = None
        resp_col = None
        
        # Find matching columns (case-insensitive)
        for col in df.columns:
            col_lower = col.lower()
            if inst_col is None and any(ic in col_lower for ic in instruction_cols):
                inst_col = col
            if resp_col is None and any(rc in col_lower for rc in response_cols):
                resp_col = col
        
        if inst_col and resp_col:
            for _, row in df.iterrows():
                if pd.notna(row[inst_col]) and pd.notna(row[resp_col]):
                    conversations.append({
                        'instruction': str(row[inst_col]),
                        'response': str(row[resp_col])
                    })
        elif len(df.columns) >= 2:
            # Use first two columns
            for _, row in df.iterrows():
                conversations.append({
                    'instruction': str(row.iloc[0]),
                    'response': str(row.iloc[1])
                })
        
        return conversations
    
    def _process_json(self, file_path: str) -> List[Dict[str, str]]:
        """Process JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return self._extract_conversations(data)
    
    def _process_jsonl(self, file_path: str) -> List[Dict[str, str]]:
        """Process JSONL file (one JSON per line)"""
        conversations = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    conv = self._extract_single_conversation(item)
                    if conv:
                        conversations.append(conv)
        
        return conversations
    
    def _extract_conversations(self, data) -> List[Dict[str, str]]:
        """Extract conversations from JSON data structure"""
        conversations = []
        
        if isinstance(data, list):
            for item in data:
                conv = self._extract_single_conversation(item)
                if conv:
                    conversations.append(conv)
        elif isinstance(data, dict):
            # Check if it's a single conversation or contains a list
            if 'data' in data:
                return self._extract_conversations(data['data'])
            elif 'conversations' in data:
                return self._extract_conversations(data['conversations'])
            else:
                conv = self._extract_single_conversation(data)
                if conv:
                    conversations.append(conv)
        
        return conversations
    
    def _extract_single_conversation(self, item: dict) -> Optional[Dict[str, str]]:
        """Extract a single conversation from a dict"""
        instruction_keys = ['instruction', 'question', 'query', 'input', 'prompt', 'user', 'human']
        response_keys = ['response', 'answer', 'output', 'reply', 'assistant', 'bot']
        
        instruction = None
        response = None
        
        for key in instruction_keys:
            if key in item:
                instruction = str(item[key])
                break
        
        for key in response_keys:
            if key in item:
                response = str(item[key])
                break
        
        if instruction and response:
            return {'instruction': instruction, 'response': response}
        
        return None
    
    def _compute_stats(self, conversations: List[Dict[str, str]]) -> Dict:
        """Compute statistics about the dataset"""
        if not conversations:
            return {'error': 'No data'}
        
        inst_lengths = [len(c['instruction']) for c in conversations]
        resp_lengths = [len(c['response']) for c in conversations]
        
        return {
            'total_samples': len(conversations),
            'avg_instruction_length': sum(inst_lengths) / len(inst_lengths),
            'avg_response_length': sum(resp_lengths) / len(resp_lengths),
            'max_instruction_length': max(inst_lengths),
            'max_response_length': max(resp_lengths),
            'total_characters': sum(inst_lengths) + sum(resp_lengths)
        }


def create_sample_healthcare_data() -> List[Dict[str, str]]:
    """Create sample healthcare Q&A data for demonstration"""
    return [
        {
            "instruction": "What are the symptoms of diabetes?",
            "response": "Common symptoms of diabetes include increased thirst, frequent urination, extreme fatigue, blurred vision, slow-healing cuts or wounds, tingling or numbness in hands and feet, and unexplained weight loss. Type 1 diabetes symptoms often develop quickly, while Type 2 symptoms may develop gradually over years."
        },
        {
            "instruction": "How do I schedule an appointment with my primary care physician?",
            "response": "To schedule an appointment with your primary care physician, you can: 1) Call our appointment line at 1-800-XXX-XXXX, 2) Log into your patient portal and use the online scheduling feature, 3) Use our mobile app to book appointments, or 4) Visit any of our care centers in person. Most routine appointments can be scheduled within 1-2 weeks."
        },
        {
            "instruction": "What is covered under my health insurance plan for preventive care?",
            "response": "Your preventive care coverage typically includes: annual wellness exams, immunizations and vaccines, cancer screenings (mammograms, colonoscopies, Pap smears), blood pressure and cholesterol screenings, diabetes screening, depression screening, and obesity counseling. These services are usually covered at 100% with no copay when using in-network providers."
        },
        {
            "instruction": "How do I refill my prescription medication?",
            "response": "You can refill your prescription by: 1) Calling the pharmacy directly with your prescription number, 2) Using our mail-order pharmacy service for 90-day supplies, 3) Logging into your patient portal and requesting a refill online, 4) Using the mobile app's refill feature, or 5) Visiting your pharmacy in person. For controlled substances, you may need a new prescription from your doctor."
        },
        {
            "instruction": "What should I do in case of a medical emergency?",
            "response": "In a medical emergency, call 911 immediately or go to the nearest emergency room. Medical emergencies include: chest pain, difficulty breathing, severe bleeding, loss of consciousness, stroke symptoms (face drooping, arm weakness, speech difficulty), severe allergic reactions, and major injuries. For non-life-threatening urgent issues, consider visiting an urgent care center."
        },
        {
            "instruction": "How can I manage my high blood pressure?",
            "response": "To manage high blood pressure: 1) Take prescribed medications as directed, 2) Reduce sodium intake to less than 2,300mg daily, 3) Exercise regularly (at least 150 minutes per week), 4) Maintain a healthy weight, 5) Limit alcohol consumption, 6) Quit smoking, 7) Manage stress through relaxation techniques, 8) Monitor your blood pressure at home regularly, and 9) Attend all follow-up appointments with your healthcare provider."
        },
        {
            "instruction": "What are the side effects of metformin?",
            "response": "Common side effects of metformin include: nausea, vomiting, diarrhea, stomach pain, loss of appetite, and metallic taste. These usually improve over time. Serious but rare side effects include lactic acidosis (seek immediate help if you experience muscle pain, weakness, difficulty breathing, or unusual tiredness) and vitamin B12 deficiency with long-term use. Always take metformin with food to reduce stomach upset."
        },
        {
            "instruction": "How do I check if a doctor is in my insurance network?",
            "response": "To verify if a doctor is in your network: 1) Log into your member portal and use the 'Find a Doctor' tool, 2) Call the customer service number on your insurance card, 3) Check our mobile app's provider directory, or 4) Ask the doctor's office directly - they can verify your coverage. Using in-network providers ensures lower out-of-pocket costs and maximum benefits."
        },
        {
            "instruction": "What is a health savings account (HSA)?",
            "response": "A Health Savings Account (HSA) is a tax-advantaged savings account for medical expenses. Benefits include: tax-free contributions, tax-free growth, and tax-free withdrawals for qualified medical expenses. To be eligible, you must have a high-deductible health plan (HDHP). HSA funds roll over year to year, are portable if you change jobs, and can be invested for long-term growth."
        },
        {
            "instruction": "How often should I get a flu shot?",
            "response": "You should get a flu shot every year, ideally in September or October before flu season peaks. The flu vaccine is reformulated annually to match circulating strains. Everyone 6 months and older should get vaccinated. It's especially important for high-risk groups: seniors, young children, pregnant women, and those with chronic health conditions. The vaccine is covered at 100% under most insurance plans."
        },
        {
            "instruction": "What mental health services are covered by insurance?",
            "response": "Mental health coverage typically includes: outpatient therapy sessions with licensed counselors or psychologists, psychiatric consultations and medication management, inpatient mental health treatment, substance abuse treatment programs, crisis intervention services, and telehealth mental health visits. Coverage is usually subject to the same copays and deductibles as physical health services under mental health parity laws."
        },
        {
            "instruction": "How do I file a claim for out-of-network services?",
            "response": "To file an out-of-network claim: 1) Obtain an itemized bill from your provider including service codes and dates, 2) Complete the claim form available on your member portal or by calling customer service, 3) Attach all receipts and medical documentation, 4) Submit via mail, fax, or upload through the member portal. Claims are typically processed within 30 days. Reimbursement is based on usual and customary rates."
        },
        {
            "instruction": "What is the difference between urgent care and emergency room?",
            "response": "Urgent care is for non-life-threatening conditions needing same-day attention: minor cuts, sprains, mild fevers, ear infections, and UTIs. Copays are typically $50-100. Emergency rooms handle life-threatening situations: chest pain, severe bleeding, stroke symptoms, major trauma, and difficulty breathing. ER copays are usually $150-500. Using urgent care for appropriate conditions saves time and money."
        },
        {
            "instruction": "How can I access my medical records?",
            "response": "To access your medical records: 1) Log into your patient portal for digital records, 2) Request records through the medical records department (forms available online or at the facility), 3) Use our mobile app to view test results and visit summaries. Under HIPAA, you have the right to access your records within 30 days of request. Electronic records are usually available immediately through the portal."
        },
        {
            "instruction": "What vaccines do adults need?",
            "response": "Recommended adult vaccines include: annual flu shot, Tdap (tetanus, diphtheria, pertussis) booster every 10 years, shingles vaccine (Shingrix) for adults 50+, pneumococcal vaccine for adults 65+ or with certain conditions, COVID-19 vaccines and boosters as recommended, and HPV vaccine for adults up to age 45 if not previously vaccinated. Your doctor may recommend additional vaccines based on your health conditions, occupation, or travel plans."
        }
    ]
