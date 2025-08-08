import csv
from langchain_core.documents import Document

# loading the data


def load_faqs(file_path="data/faqs.csv"):
    documents = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row.get("Question").strip()
            answer = row.get("Answer").strip()
            combined_text = f"Question: {question}\nAnswer: {answer}"
            doc = Document(page_content=combined_text,
                           metadata={"question": question})
            documents.append(doc)

    return documents
