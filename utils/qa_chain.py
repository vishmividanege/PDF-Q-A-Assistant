from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import HuggingFacePipeline

def load_local_llm():
    """Load a local HuggingFace model instead of OpenAI."""
    from transformers import pipeline

    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        temperature=0,
        max_length=256
    )
    return HuggingFacePipeline(pipeline=pipe)

def make_qa_chain():
    """
    Creates a QA chain using a local LLM without a vector store.
    """
    llm = load_local_llm()

    from langchain_classic.prompts import PromptTemplate
    prompt = PromptTemplate(
        template="Answer the question based on the context below:\n\n{context}\n\nQuestion: {question}\nAnswer:",
        input_variables=["context", "question"]
    )

    # Only combine docs chain, no retriever needed
    combine_docs = create_stuff_documents_chain(llm=llm, prompt=prompt)

    return combine_docs  # This acts as your QA chain

def answer_question(qa_chain, question, context):
    """
    qa_chain: combine_docs_chain (no retriever)
    question: user's question
    context: full text from the PDF
    """
    result = qa_chain.invoke({
        "context": context,
        "question": question
    })
    return result
