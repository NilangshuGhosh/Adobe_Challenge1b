import os
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import json

# STEP 1: Read persona from file
def read_persona(file_path="C:\\Users\\NILANGSHU\\OneDrive\\Desktop\\New folder\\Python\\adobe_round1b\\persona.txt"):
    with open(file_path, 'r', encoding='utf-8') as f:
        persona_text = f.read()
    print("\n🔍 Persona Description:\n", persona_text)
    return persona_text

# STEP 2: Read all PDFs and split into sections
def read_all_pdfs(folder="C:\\Users\\NILANGSHU\\OneDrive\\Desktop\\New folder\\Python\\adobe_round1b\\input_folder"):
    all_docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder, filename)
            print(f"\n📄 Reading {filename} ...")
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                sections = text.split("\n\n")  # split by paragraphs
                print(f"✅ Extracted {len(sections)} sections from {filename}")
                all_docs[filename] = sections
            except Exception as e:
                print(f"❌ Failed to read {filename}: {e}")
    return all_docs

# STEP 3: Main processing
if __name__ == "__main__":
    # Load persona and documents
    persona = read_persona()
    pdf_sections = read_all_pdfs()

    # Load model
    print("\n🧠 Loading sentence-transformer model...")
    model = SentenceTransformer("local_model")
    # model = SentenceTransformer("all-MiniLM-L6-v2")
    # # model = SentenceTransformer("all-MiniLM-L6-v2")
    # model.save("local_model")
    # Encode persona once
    persona_embedding = model.encode(persona, convert_to_tensor=True)

    output = {
        "persona": persona.strip(),
        "documents": []
    }

    print("\n🔎 Scoring sections for relevance...")

    for filename, sections in pdf_sections.items():
        scored_sections = []
        for section in sections:
            section = section.strip()
            if len(section) < 50:
                continue  # skip short sections
            section_embedding = model.encode(section, convert_to_tensor=True)
            score = util.cos_sim(persona_embedding, section_embedding).item()
            if score > 0.4:  # filter low-relevance
                scored_sections.append({
                    "section_title": section.split("\n")[0][:60],
                    "content_snippet": section[:300],
                    "score": round(score, 3)
                })

        # Sort and pick top 3
        scored_sections = sorted(scored_sections, key=lambda x: x["score"], reverse=True)[:3]

        output["documents"].append({
            "filename": filename,
            "relevance_score": round(sum(s["score"] for s in scored_sections)/3, 3) if scored_sections else 0.0,
            "top_sections": scored_sections
        })

    # Sort final output by doc relevance
    output["documents"] = sorted(output["documents"], key=lambda x: x["relevance_score"], reverse=True)

    # Save to output.json
    with open("challenge1b_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n✅ All done! Output written to output.json")




# import os
# import fitz  # pymupdf

# # STEP 1: Read the persona.txt file
# def read_persona(file_path="C:\\Users\\NILANGSHU\\OneDrive\\Desktop\\New folder\\Python\\adobe_round1b\\persona.txt"):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         persona_text = f.read()
#     print("\n🔍 Persona Description:\n", persona_text)
#     return persona_text

# # STEP 2: Read text from all PDFs in input_folder
# def read_all_pdfs(folder="C:\\Users\\NILANGSHU\\OneDrive\\Desktop\\New folder\\Python\\adobe_round1b\\input_folder"):
#     all_docs = {}
#     for filename in os.listdir(folder):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(folder, filename)
#             print(f"\n📄 Reading {filename} ...")
#             doc = fitz.open(file_path)
#             text = ""
#             for page in doc:
#                 text += page.get_text()
#             all_docs[filename] = text
#             print(f"✅ Extracted {len(text)} characters.")
#     return all_docs

# # Main execution
# if __name__ == "__main__":
#     persona = read_persona()
#     pdf_texts = read_all_pdfs()
