from nltk.tokenize import sent_tokenize
def to_do(txt):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", 
    "today", "tomorrow", "yesterday", "week", "Today", "Tomorrow", "Yesterday", "Week", "morning", "evening", "afternoon", "Morning", "Evening", "Afternoon"]
    sentences = sent_tokenize(txt)
    todo_sentences = []
    for sent in sentences:
        for day in weekdays:
            if day in sent:
                todo_sentences.append(sent)
                break
    for sent in sentences:
        for character in sent:
            if character.isdigit():
                todo_sentences.append(sent)
                break
    return " ".join(list(set(todo_sentences)))
    
            