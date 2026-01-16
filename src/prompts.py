def basic_prompt(schema_text: str, question: str) -> str:
    """
    Create a basic prompt for converting natural language question to SQL.
    
    Args:
        schema_text: Database schema as formatted text
        question: Natural language question
        
    Returns:
        Formatted prompt string
    """
    prompt = f"Database schema:\n{schema_text}\n\nQuestion: {question}\n\nConvert to SQL. Make sure the syntax is correct:"
    return prompt


def few_shot_prompt(schema_text: str, question: str) -> str:
    """
    Create a few-shot prompt with examples for converting natural language to SQL.
    
    Args:
        schema_text: Database schema as formatted text
        question: Natural language question
        
    Returns:
        Formatted prompt string with examples
    """
    examples = """
Example 1:
Question: How many customers does each country have?
SQL: SELECT Country, COUNT(*) as CustomerCount FROM Customer GROUP BY Country ORDER BY CustomerCount DESC

Example 2:
Question: What are the top 5 best-selling genres by total sales?
SQL: SELECT g.Name, SUM(il.UnitPrice * il.Quantity) as TotalSales FROM Genre g JOIN Track t ON g.GenreId = t.GenreId JOIN InvoiceLine il ON t.TrackId = il.TrackId GROUP BY g.Name ORDER BY TotalSales DESC LIMIT 5

Example 3:
Question: List all albums by the artist 'AC/DC'
SQL: SELECT al.Title FROM Album al JOIN Artist ar ON al.ArtistId = ar.ArtistId WHERE ar.Name = 'AC/DC'
"""
    
    prompt = f"""
You are an AI assistant that converts natural language questions into SQL queries.
You will be given a database schema and a question. Your task is to generate a correct SQL query that answers the question using the provided schema.

<schema>  
{schema_text}  
</schema>

<question>  
{question}
</question>

Here are a few examples of how to convert natural language questions to SQL queries:
<examples>
{examples}
</examples>

Keep in mind the following:
- Output your final SQL query inside `<sql_query>` tags
- Use the examples to help you convert the natural language question to SQL.
- Use the schema to help you convert the natural language question to SQL.
- Use the question to help you convert the natural language question to SQL.

<sql_query>
[Your SQL query here]
</sql_query>
"""
    
    return prompt


def agentic_prompt(schema_text: str, question: str) -> str:
    """
    Create an agentic prompt that demonstrates iterative reasoning and self-correction.
    Simplified to focus on SQL output while showing agentic thinking.
    
    Args:
        schema_text: Database schema as formatted text
        question: Natural language question
        
    Returns:
        Formatted prompt string with agentic reasoning steps
    """
    prompt = f"""
You are an AI SQL assistant. Think through the problem step-by-step, then generate the SQL query.

<schema>
{schema_text}
</schema>

<question>
{question}
</question>

Before generating SQL, think about:
1. What tables and columns are needed?
2. What joins are required?
3. What filters or aggregations are needed?
4. Verify table and column names match the schema exactly.

After thinking, output ONLY the SQL query inside <sql_query> tags. Do not include any explanation or reasoning text.

<sql_query>
[Your SQL query here]
</sql_query>
"""
    return prompt

