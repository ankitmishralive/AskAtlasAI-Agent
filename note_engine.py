


from llama_index.core.tools import FunctionTool

import os 

note_file = os.path.join("data","notes.txt")


def save_note(note):
    # if not os.path.exists()
    if not os.path.exists(note_file):
        open(note_file, "w")
    
    with open(note_file, "a") as  f:  # a -> append 
        f.writelines([note+"\n"])


    return "Note Saved"



note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="this tool can save a text based note to a file for the user",
)



# from llama_index.core.tools import FunctionTool
# import os 

# note_file = os.path.join("data", "notes.txt")

# def save_note(note):
#     """
#     Saves a text-based note to a file.

#     Parameters:
#         note (str): The note to be saved.

#     Returns:
#         str: Confirmation message or error description.
#     """
#     try:
#         # Ensure the file exists
#         if not os.path.exists(note_file):
#             with open(note_file, "w"):
#                 pass
#         # Append the note
#         with open(note_file, "a") as f:
#             f.writelines([note + "\n"])
#         return "Note Saved"
#     except Exception as e:
#         return f"Failed to save note: {str(e)}"

# # Define the tool
# note_engine = FunctionTool.from_defaults(
#     fn=save_note,
#     name="note_saver",
#     description="This tool can save a text-based note to a file for the user.",
# )
