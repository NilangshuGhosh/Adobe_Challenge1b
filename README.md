# Adobe_Challenge1b
Adobe hackathon project.

You're working on a system that:

Loads multiple PDF documents.

Embeds them using a transformer model (sentence-transformers).

Stores those embeddings.

Takes a JSON query (with a "persona") as input.

Uses the query to rank the most relevant document sections based on cosine similarity.

Outputs a result JSON with filenames and relevant content snippets.

🧠 Command-line Arguments Explained
Your code is designed to be run like this from terminal:

bash
Copy
Edit
python solve_round1b.py --docs_dir=./docs --query_file=input.json --output_file=output.json
Here’s what each argument means:

1. --docs_dir=./docs
Purpose: Path to the folder containing your .pdf documents.

Example: ./docs means all PDFs in the folder named docs (in the current directory) will be read.

Challenge: Make sure only PDFs are in this folder, or code might try to read invalid files.

2. --query_file=input.json
Purpose: Path to your query input file (usually in JSON).

Contents: Should include:

json
Copy
Edit
{
  "persona": "Some persona description or task"
}
Challenge: The file must be valid JSON with a "persona" key, or the program will crash or behave unexpectedly.

3. --output_file=output.json
Purpose: Path to write the final output results in JSON format.

Output Includes:

Relevance scores for each document.

Best-matching sections from top files.

File names.

Challenge: Make sure the directory you write to exists; if not, Python will throw a FileNotFoundError.

⚠ Common Issues and Mistakes
Problem	Cause	Fix
error: unrecognized arguments	You misspelled an argument name	Use double dashes (--) and check spelling
PDF not read	PDF is encrypted or corrupted	Use a simpler or re-exported PDF
KeyError: 'persona'	JSON input file missing "persona" key	Check input file format
Output file is empty	All cosine scores were zero or low	Try stronger query phrasing
Stuck terminal	Python process didn’t release	Use Ctrl+C to stop or restart terminal


If you want to test without command-line arguments, add the following block to the bottom of your solve_round1b.py file:

python
Copy
Edit
if _name_ == "_main_":
    import sys
    sys.argv = ["solve_round1b.py", 
                "--docs_dir=./docs", 
                "--query_file=input.json", 
                "--output_file=output.json"]
    main()
This simulates the arguments and lets you just run:

bash
Copy
Edit
python solve_round1b.py
in the terminal with no flags needed.

