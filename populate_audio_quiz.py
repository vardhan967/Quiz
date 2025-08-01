import os
import django

# Set up the Django environment
# This is necessary to use the Django models outside of the manage.py runserver command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quiz_Base.settings')
django.setup()

from Quiz_App.models import Category, Question, Answer

def populate_audio_engineering_quiz():
    """
    This function creates a new quiz category 'Audio Engineering' and populates it
    with a set of questions and their corresponding answers.
    """
    # --- 1. Define the Quiz Data ---
    # A list of dictionaries, where each dictionary represents a question and its answers.
    audio_questions = [
        # Original Questions
        {
            "question": "What does a compressor do in audio processing?",
            "answers": [("Reduces the dynamic range", True), ("Increases the stereo width", False), ("Adds reverberation", False), ("Filters out high frequencies", False)], "marks": 1
        },
        {
            "question": "Which of these is a common type of microphone?",
            "answers": [("Dynamic", True), ("Kinetic", False), ("Static", False), ("Potential", False)], "marks": 1
        },
        {
            "question": "What is the standard sample rate for CD quality audio?",
            "answers": [("44.1 kHz", True), ("22.05 kHz", False), ("48 kHz", False), ("96 kHz", False)], "marks": 1
        },
        {
            "question": "What does 'EQ' stand for in audio engineering?",
            "answers": [("Equalization", True), ("Energy Quotient", False), ("Echo Quality", False), ("External Quantizer", False)], "marks": 1
        },
        {
            "question": "Which audio effect is used to create a sense of space or environment?",
            "answers": [("Reverb", True), ("Chorus", False), ("Flanger", False), ("Distortion", False)], "marks": 1
        },
        # New Questions
        {
            "question": "What does the 'attack' parameter on a compressor control?",
            "answers": [("How quickly the compressor starts working", True), ("How long the compression lasts", False), ("The amount of gain reduction", False), ("The volume of the output signal", False)], "marks": 1
        },
        {
            "question": "A cardioid microphone is most sensitive to sound from which direction?",
            "answers": [("The front", True), ("The rear", False), ("The sides", False), ("All directions equally", False)], "marks": 1
        },
        {
            "question": "What is 'phantom power' used for?",
            "answers": [("Powering condenser microphones", True), ("Creating artificial reverb", False), ("Reducing feedback", False), ("Powering guitar pedals", False)], "marks": 1
        },
        {
            "question": "In digital audio, what does 'bit depth' determine?",
            "answers": [("The dynamic range of the recording", True), ("The frequency range of the recording", False), ("The length of the recording", False), ("The stereo width", False)], "marks": 1
        },
        {
            "question": "Which frequency range is typically considered 'bass'?",
            "answers": [("20 Hz - 250 Hz", True), ("250 Hz - 2 kHz", False), ("2 kHz - 6 kHz", False), ("6 kHz - 20 kHz", False)], "marks": 1
        },
        {
            "question": "What is the primary purpose of a 'pop filter'?",
            "answers": [("To reduce plosives (p-pops)", True), ("To make vocals sound louder", False), ("To filter out low frequencies", False), ("To protect the microphone from dust", False)], "marks": 1
        },
        {
            "question": "The Haas effect is related to which aspect of sound perception?",
            "answers": [("Localization and stereo imaging", True), ("Pitch perception", False), ("Loudness perception", False), ("Timbre perception", False)], "marks": 1
        },
        {
            "question": "What does a 'gate' or 'noise gate' do?",
            "answers": [("Mutes a signal when it falls below a certain volume", True), ("Boosts a signal when it falls below a certain volume", False), ("Adds noise to a signal", False), ("Inverts the phase of a signal", False)], "marks": 1
        },
        {
            "question": "Which of these is a 'balanced' audio connector?",
            "answers": [("XLR", True), ("RCA", False), ("3.5mm TS", False), ("Guitar jack (1/4\" TS)", False)], "marks": 1
        },
        {
            "question": "What is 'dithering' used for in audio?",
            "answers": [("Reducing quantization error when lowering bit depth", True), ("Increasing the sample rate", False), ("Creating a tremolo effect", False), ("Synchronizing two digital devices", False)], "marks": 1
        },
        {
            "question": "Which type of EQ has a 'Q' parameter to control its bandwidth?",
            "answers": [("Parametric EQ", True), ("Graphic EQ", False), ("Shelving EQ", False), ("High-pass filter", False)], "marks": 1
        },
        {
            "question": "What is the main purpose of 'acoustic treatment' in a room?",
            "answers": [("To control reflections and reverb", True), ("To make the room completely silent", False), ("To amplify sound", False), ("To change the pitch of the sound", False)], "marks": 1
        },
        {
            "question": "In a DAW, what does MIDI stand for?",
            "answers": [("Musical Instrument Digital Interface", True), ("Music Information Data Input", False), ("Mastering Interface for Digital Integration", False), ("Multi-track Interactive Digital Instrument", False)], "marks": 1
        },
        {
            "question": "A 'De-Esser' is a type of compressor specifically designed to target what?",
            "answers": [("Sibilance (harsh 's' sounds)", True), ("Low-frequency hum", False), ("Background noise", False), ("Vocal breaths", False)], "marks": 1
        },
        {
            "question": "What is latency in the context of digital audio recording?",
            "answers": [("The delay between an input and its audible output", True), ("The maximum volume a track can reach", False), ("The process of aligning tracks in time", False), ("A type of audio file compression", False)], "marks": 1
        },
    ]

    print("Starting to populate the Audio Engineering quiz...")

    # --- 2. Create or Get the Category ---
    category, created = Category.objects.get_or_create(name="Audio Engineering")

    # === FIX IS HERE ===
    if created:
        print(f"Category '{category.name}' created.")
        # If the category is new, there are no existing questions.
        existing_questions = set()
    else:
        print(f"Category '{category.name}' already exists.")
        # If the category exists, get the set of questions to avoid duplicates.
        existing_questions = set(Question.objects.filter(category=category).values_list('question_text', flat=True))


    # --- 3. Loop Through Questions and Create Database Objects ---
    new_questions_added = 0
    for q_data in audio_questions:
        question_text = q_data["question"]
        
        # This check will now work correctly in all cases
        if question_text not in existing_questions:
            question_marks = q_data["marks"]

            # Create the Question object
            question = Question.objects.create(
                category=category,
                question_text=question_text,
                marks=question_marks
            )
            print(f"  - Creating question: {question.question_text}")
            new_questions_added += 1

            # Create the corresponding Answer objects
            for a_text, is_correct in q_data["answers"]:
                Answer.objects.create(
                    question=question,
                    answer_text=a_text,
                    is_correct=is_correct
                )

    print("\nPopulation complete!")
    if new_questions_added > 0:
        print(f"Added {new_questions_added} new questions to the '{category.name}' category.")
    else:
        print("No new questions were added as they already exist in the database.")


# --- Run the script ---
if __name__ == '__main__':
    populate_audio_engineering_quiz()
