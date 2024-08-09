import streamlit as st
from sqlalchemy.orm import Session
from database import init_db, SessionLocal, Document, UserHistory
from utils import save_file, process_document, encrypt, decrypt


init_db()

def main():
    st.title("Document Querying App")

    st.sidebar.header("Upload Documents")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        file_path = f"temp/{uploaded_file.name}"
        save_file(uploaded_file, file_path)
        content = process_document(file_path)
        
       
        db = SessionLocal()
        doc = Document(name=uploaded_file.name, content=encrypt(content))
        db.add(doc)
        db.commit()
        db.close()
        st.success(f"Document '{uploaded_file.name}' uploaded successfully!")

    st.sidebar.header("Query History")
    user_id = st.sidebar.text_input("Enter your user ID", value="1")  

    st.subheader("Ask a Question")
    query = st.text_input("Your Query:")
    
    if st.button("Submit Query"):
        db = SessionLocal()
        documents = db.query(Document).all()
        responses = []

        for doc in documents:
            decrypted_content = decrypt(doc.content)
            if query.lower() in decrypted_content.lower():
                responses.append(f"Found in '{doc.name}'")
        
        if responses:
            for response in responses:
                st.write(response)
           
            history = UserHistory(user_id=user_id, query=query, response=", ".join(responses))
            db.add(history)
            db.commit()
        else:
            st.write("No matching documents found.")

        db.close()

    st.subheader("Download Query History")
    if st.button("Download History"):
        db = SessionLocal()
        history_records = db.query(UserHistory).filter(UserHistory.user_id == user_id).all()
        db.close()

        history_df = pd.DataFrame([(h.query, h.response) for h in history_records], columns=["Query", "Response"])
        history_df.to_csv("query_history.csv", index=False)
        
        with open("query_history.csv", "rb") as file:
            st.download_button("Download Query History", file, file_name="query_history.csv")

if __name__ == "__main__":
    main()
