# Thees functions are for constructing and deconstructing files. 
# The capstone project sends byte arrays, so you will need to convert a file into a byte array before sending it.
# Once the file is received, convert it back into a file and save it.

# deconstruct_file --> Takes a file path as an input. 
# - Converts the file into a byte array
# - Returns the byte array

# construct_file
# - Converts a byte array back into a file. 

def deconstruct_file(file_path):
    print(f"Converting {file_path} to a byte array...")

    #fileName, fileExtension = os.path.splitext(filePath)

    # Open the file
    with open(file_path, 'rb') as file_t:

        # Convert the file to a byte array
        blob_data = bytearray(file_t.read())
        return blob_data
    
def construct_file(byte_array, save_location, file_extension):  
       
    # Convert the byte array to a new file
    with open((save_location) + file_extension, "wb") as newFile:
        newFile.write(byte_array)
        newFile.close()   
            
    return
