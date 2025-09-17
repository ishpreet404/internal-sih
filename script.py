from ocr import extract_document_text
from llm_summarizer import create_document_summary
import load_env  # Load environment variables from .env file
import os

# Set up paths
pdf_path = os.path.join(os.getcwd(), "MALAYALAM.pdf")
output_dir = os.path.join(os.getcwd(), "output")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

print(f"PDF path: {pdf_path}")
print(f"Output directory: {output_dir}")
print(f"PDF exists: {os.path.exists(pdf_path)}")

try:
    # Extract text from PDF
    print("\n🔍 Extracting text from PDF...")
    page_texts, combined_text = extract_document_text(
        file_path=pdf_path,
        output_dir=output_dir,
        tesseract_langs='mal+eng'  # Malayalam + English
    )

    # Access results
    print(f"✅ Extracted {len(page_texts)} pages")
    print(f"📊 Combined text length: {len(combined_text)} characters")

    # Display language detection results
    print("\n🌍 Language Detection:")
    for page_num, info in page_texts.items():
        print(f"  Page {page_num}: {info['language']} (via {info['method']})")

    # Display sample of page 1
    if 1 in page_texts:
        print("\n📄 Sample from Page 1:")
        print(page_texts[1]['marked_text'][:300] + "..." if len(page_texts[1]['marked_text']) > 300 else page_texts[1]['marked_text'])

    # Generate GitHub LLM summary
    print("\n🤖 Generating AI Summary using GitHub LLM...")
    summary_data = create_document_summary(page_texts, combined_text, output_dir)

    if "error" not in summary_data:
        print("✅ AI Summary Generated Successfully!")
        print(f"\n📋 Document Type: {summary_data['document_type']}")
        print(f"\n📝 Overall Summary:\n{summary_data['overall_summary']}")

        print("\n🔑 Key Information:")
        for category, items in summary_data['key_information'].items():
            if items:
                print(f"  {category.replace('_', ' ').title()}: {', '.join(items)}")

        print("\n📊 Metadata:")
        print(f"  Total Pages: {summary_data['metadata']['total_pages']}")
        print(f"  Total Characters: {summary_data['metadata']['total_characters']}")
        print(f"  Languages Detected: {', '.join(summary_data['metadata']['languages_detected'])}")

        print(f"\n💾 Summary files saved to: {output_dir}")
        print("  - document_summary.json (detailed JSON)")
        print("  - document_summary.txt (readable format)")

    else:
        print(f"❌ Error generating AI summary: {summary_data['error']}")
        print("💡 Make sure you have set your GITHUB_TOKEN environment variable")
        print("   You can get a GitHub token from: https://github.com/settings/tokens")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()