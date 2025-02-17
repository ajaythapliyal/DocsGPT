from pathlib import Path
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import dotenv
import ast
import typer
import tiktoken

dotenv.load_dotenv()

def get_functions(source_code):
    tree = ast.parse(source_code)
    functions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = ast.unparse(node)

    return functions

def get_functions_names(node):
    functions = []
    for child in node.body:
        if isinstance(child, ast.FunctionDef):
            functions.append(child.name)
    return functions



def get_classes(source_code):
    tree = ast.parse(source_code)
    classes = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes[node.name] = get_functions_names(node)
    return classes

def get_functions_in_class(source_code, class_name):
    tree = ast.parse(source_code)
    functions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name == class_name:
                for function in node.body:
                    if isinstance(function, ast.FunctionDef):
                        functions.append(function.name)
    return functions


def parse_functions(functions_dict):
    c1 = len(functions_dict)
    c2 = 0
    for source, functions in functions_dict.items():
        c2 += 1
        print(f"Processing file {c2}/{c1}")
        f1 = len(functions)
        f2 = 0
        source_w = source.replace("inputs/", "")
        source_w = source_w.replace(".py", ".md")
        # this is how we check subfolders
        if "/" in source_w:
            subfolders = source_w.split("/")
            subfolders = subfolders[:-1]
            subfolders = "/".join(subfolders)
            if not Path(f"outputs/{subfolders}").exists():
                Path(f"outputs/{subfolders}").mkdir(parents=True)

        for name, function in functions.items():
            f2 += 1
            print(f"Processing function {f2}/{f1}")
            prompt = PromptTemplate(
                input_variables=["code"],
                template="Code: \n{code}, \nDocumentation: ",
            )
            llm = OpenAI(temperature=0)
            response = llm(prompt.format(code=function))

            if not Path(f"outputs/{source_w}").exists():
                with open(f"outputs/{source_w}", "w") as f:
                    f.write(f"# Function name: {name} \n\nFunction: \n```\n{function}\n```, \nDocumentation: \n{response}")
            else:
                with open(f"outputs/{source_w}", "a") as f:
                    f.write(f"\n\n# Function name: {name} \n\nFunction: \n```\n{function}\n```, \nDocumentation: \n{response}")


def parse_classes(classes_dict):
    c1 = len(classes_dict)
    c2 = 0
    for source, classes in classes_dict.items():
        c2 += 1
        print(f"Processing file {c2}/{c1}")
        f1 = len(classes)
        f2 = 0
        source_w = source.replace("inputs/", "")
        source_w = source_w.replace(".py", ".md")

        if "/" in source_w:
            subfolders = source_w.split("/")
            subfolders = subfolders[:-1]
            subfolders = "/".join(subfolders)
            if not Path(f"outputs/{subfolders}").exists():
                Path(f"outputs/{subfolders}").mkdir(parents=True)

        for name, function_names in classes.items():
            print(f"Processing Class {f2}/{f1}")
            f2 += 1
            prompt = PromptTemplate(
                input_variables=["class_name", "functions_names"],
                template="Class name: {class_name} \nFunctions: {functions_names}, \nDocumentation: ",
            )
            llm = OpenAI(temperature=0)
            response = llm(prompt.format(class_name=name, functions_names=function_names))

            if not Path(f"outputs/{source_w}").exists():
                with open(f"outputs/{source_w}", "w") as f:
                    f.write(f"# Class name: {name} \n\nFunctions: \n{function_names}, \nDocumentation: \n{response}")
            else:
                with open(f"outputs/{source_w}", "a") as f:
                    f.write(f"\n\n# Class name: {name} \n\nFunctions: \n{function_names}, \nDocumentation: \n{response}")


#User permission
def transform_to_docs(functions_dict, classes_dict):
# Function to ask user permission to call the OpenAI api and spend their OpenAI funds.
    # Here we convert dicts to a string and calculate the number of OpenAI tokens the string represents.
    docs_content = ""
    for key, value in functions_dict.items():
        docs_content += str(key) + str(value)
    for key, value in classes_dict.items():
        docs_content += str(key) + str(value)

    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(docs_content))
    total_price = ((num_tokens / 1000) * 0.02)

    # Here we print the number of tokens and the approx user cost with some visually appealing formatting.
    print(f"Number of Tokens = {format(num_tokens, ',d')}")
    print(f"Approx Cost = ${format(total_price, ',.2f')}")
    #Here we check for user permission before calling the API.
    user_input = input("Price Okay? (Y/N) \n").lower()
    if user_input == "y":
        if not Path("outputs").exists():
            Path("outputs").mkdir()
        parse_functions(functions_dict)
        print("Functions done!")
        parse_classes(classes_dict)
        print("All done!")
    elif user_input == "":
        if not Path("outputs").exists():
            Path("outputs").mkdir()
        parse_functions(functions_dict)
        print("Functions done!")
        parse_classes(classes_dict)
        print("All done!")
    else:
        print("The API was not called. No money was spent.")