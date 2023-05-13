 
 #-------------------Plant Disease Detection Model for Tomato leaf classified as healthy and infected-------------------#

#Model Implementation

#Importing and Model Build 

# TensorFlow is required for Keras to work
#Importing Keras model to load

from keras.models import load_model  

# Install pillow instead of PIL

from PIL import Image, ImageOps

#Importing numpy and Tkinter packages

import numpy as np
import tkinter as tk

from tkinter import filedialog
from tkinter import ttk




#Model Configuration 


def Predict(x):

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Loading the model
    model = load_model("keras_Model.h5", compile=False)

    # Loading the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    print(x)

    # Replace this with the image path
    image = Image.open("{}".format(x)).convert("RGB")

    # Resizing the image to be at least 224x224 and image processing
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Turning image into a numpy array
    image_array = np.asarray(image)

    # Normalizing image array
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Loading the image into the array
    data[0] = normalized_image_array

    # Model Prediction Config

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]


    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)


    return [class_name[2:],confidence_score]



#Tkinter Configuration and Screen Model Specs

from PIL import Image, ImageTk



class LeafDetectorApp:
    def __init__(self, master):

        # Setting window title
        master.title("  AGRODETECT")

        # Getting screen dimensions and calculating window size and position
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        window_width =  1500
        window_height = 1000

        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2

        # Setting window size and position
        master.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        # Creating rounded button styles
        rounded_style = {"borderwidth": 2, "relief": "groove", "font": ("Helvetica", 12), "padx": 10, "pady": 5}

        # Creating button for upload
        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()


        # Creating image labels
        self.image_label = tk.Label(master)
        self.image_label.pack()


        # Creation of predict button
        self.predict_button = tk.Button(master, text="Predict", command=self.predict)
        self.predict_button.pack()


        # Creating prediction text box
        self.prediction_text = tk.Text(master, height=25, width=140)
        self.prediction_text.pack()

    
        # Creating quit button
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()



#Tkinter Image Upload Conifguration


    def upload_image(self):

        # Opens file dialog to choose image file
        file_path = filedialog.askopenfilename()


        # If a file was chosen, display it and save its path
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)

            # Resize image to fit labels

            image.thumbnail((400, 400)) 
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

#Predictyion classes

    def predict(self):

        # Do prediction on self.image_path and display result in prediction_text
        
        result = Predict(self.image_path)
        x = result[0].split("\n")
        remedy = ''
        if x[0]=='Healthy':
            remedy = "\t\t\t\t\tCrop is totally healthy. \n\t\t\t\t\tHappy Farming!!"
        elif x[0]== "Yellow Leaf Virus":
            remedy = """ 
            \n1. Remove and destroy infected plants: Infected plants should be removed from the garden and destroyed to prevent the spread of the virus to healthy plants. Do not compost infected plant material.
            \n2.Use virus-resistant varieties: Some tomato varieties are resistant to the virus and can be planted to reduce the risk of infection.
            \n3.Control the whitefly population: \nThe whitefly is the primary vector for the tomato leaf curl virus, so controlling their population is essential. \nUse insecticidal soap or neem oil to control whiteflies. \nYellow sticky traps can also be used to trap whiteflies.
            \n4.Practice good garden hygiene: Clean and sanitize your gardening tools and equipment regularly to prevent the spread of the virus.
            \n5. Keep plants healthy: Healthy plants are better able to resist disease. Provide plants with appropriate water, nutrients, and sunlight.
            """
        elif x[0]== "Mosaic Virus":
            remedy = """
            \n1.Remove and destroy infected plants: Infected plants should be removed from the garden and destroyed to prevent the spread of the virus to healthy plants. Do not compost infected plant material.
            \n2.Use virus-resistant varieties: Some tomato varieties are resistant to the virus and can be planted to reduce the risk of infection.
            \n3.Control aphid populations: Aphids are the primary vector for the tomato mosaic virus, so controlling their population is essential. \nUse insecticidal soap or neem oil to control aphids. Yellow sticky traps can also be used to trap aphids.
            \n4.Practice good garden hygiene: Clean and sanitize your gardening tools and equipment regularly to prevent the spread of the virus.
            \n5.Keep plants healthy: Healthy plants are better able to resist disease. Provide plants with appropriate water, nutrients, and sunlight.
            """
        elif x[0]== "Spider Mites":
            remedy = """
            \n1.Spray with water: A strong stream of water can help dislodge spider mites from the plants. \nSpray the plants thoroughly, making sure to target the undersides of the leaves.
            \n2.Use insecticidal soap: Insecticidal soap can be effective at controlling spider mites. \nBe sure to follow the label instructions carefully.
            \n3.Apply neem oil: Neem oil is a natural pesticide that can control spider mites. \nDilute the neem oil according to the label instructions and apply to the plants.
            \n4.Release predatory mites: Predatory mites, such as Phytoseiulus persimilis, can be released onto the plants to feed on the spider mites. \nBe sure to follow the release instructions carefully.
            \n5.Remove heavily infested leaves: If a plant is heavily infested with spider mites, it may be best to remove the affected leaves to prevent the spread of the infestation to other plants.
            \n6.Practice good garden hygiene: Spider mites thrive in dusty conditions, so keep the garden free of debris and weeds. \nAdditionally, keep the plants well-watered to help prevent stress, which can make them more susceptible to infestations.
            """
        elif x[0]== "Septoria Leaf Spot":
            remedy = """
            \n1.Remove infected leaves: Remove infected leaves from the plant as soon as they are noticed. \nThis will help prevent the spread of the disease to other parts of the plant and other plants in the garden.
            \n2.Keep plants well-spaced: Good air circulation can help prevent the spread of the disease. \nPlant tomato plants far enough apart to ensure good air circulation.
            \n3.Mulch around plants: Mulch can help prevent the spread of the fungus from the soil to the leaves. \nApply a layer of mulch around the plants, but do not let it touch the stems.
            \n4.Water at the base of the plant: Water the plants at the base to prevent the leaves from getting wet. \nWet leaves can promote the growth of the fungus.
            \n5.Apply fungicides: Fungicides can be effective in controlling septoria leaf spot. Be sure to follow the label instructions carefully.
            \n6.Practice good garden hygiene: Clean up debris and plant material from the garden regularly to prevent the buildup of fungal spores. \nAdditionally, clean and sanitize gardening tools regularly. 
            """
        elif x[0]== "Leaf Mold":
            remedy = """
            \n1.Water at the base of the plant: Water the plants at the base to prevent the leaves from getting wet. \nWet leaves can promote the growth of the fungus.
            \n2.Space plants properly: Good air circulation can help prevent the spread of the disease. \nPlant tomato plants far enough apart to ensure good air circulation.
            \n3.Apply fungicides: Fungicides can be effective in controlling leaf mold. \nBe sure to follow the label instructions carefully.
            \n4.Use disease-resistant varieties: Some tomato varieties are resistant to leaf mold and can be planted to reduce the risk of infection.
            \n5.Remove infected leaves: Remove infected leaves from the plant as soon as they are noticed. \nThis will help prevent the spread of the disease to other parts of the plant and other plants in the garden.
            \n6.Practice good garden hygiene: Clean up debris and plant material from the garden regularly to prevent the buildup of fungal spores. \nAdditionally, clean and sanitize gardening tools regularly. 
            """
        elif x[0]== "Early Blight":
            remedy = """
            \n1.Use disease-resistant varieties: Some tomato varieties are resistant to early blight and can be planted to reduce the risk of infection.
            \n2.Rotate crops: Do not plant tomatoes in the same location in the garden every year. \nRotate crops to prevent the buildup of fungal spores in the soil.
            \n3.Mulch around plants: Mulch can help prevent the spread of the fungus from the soil to the leaves. \n\nApply a layer of mulch around the plants, but do not let it touch the stems.
            \n4.Remove infected leaves: Remove infected leaves from the plant as soon as they are noticed. \nThis will help prevent the spread of the disease to other parts of the plant and other plants in the garden.
            \n5.Apply fungicides: Fungicides can be effective in controlling early blight. \nBe sure to follow the label instructions carefully.
            \n6.Practice good garden hygiene: Clean up debris and plant material from the garden regularly to prevent the buildup of fungal spores. \nAdditionally, clean and sanitize gardening tools regularly. 
            """
        elif x[0]== "Bacterial Spot":
            remedy = """
            \n1.Use disease-resistant varieties: Some tomato varieties are resistant to bacterial spot and can be planted to reduce the risk of infection.
            \n2.Rotate crops: Do not plant tomatoes in the same location in the garden every year. Rotate crops to prevent the buildup of bacteria in the soil.
            \n3.Practice good garden hygiene: Clean up debris and plant material from the garden regularly to prevent the buildup of bacteria.\n Additionally, clean and sanitize gardening tools regularly.
            \n4.Water at the base of the plant: Water the plants at the base to prevent the leaves from getting wet.  Wet leaves can promote the growth of bacteria.
            \n5.Space plants properly: Good air circulation can help prevent the spread of the disease. \nPlant tomato plants far enough apart to ensure good air circulation.
            \n6.Remove infected leaves: Remove infected leaves and stems from the plant as soon as they are noticed. This will help prevent the spread of the disease to other parts of the plant and other plants in the garden.
            \n7.Consider copper-based sprays: Copper-based sprays can help control bacterial spot, but should be used with caution as they can build up in the soil over time. 
            """

#Accuracy class 

        self.prediction_text.insert(tk.END, """
        Class: {0}
        Accuracy: {1}
        --------------------
        Remedy:\n {2}
        """.format(result[0], result[1], remedy))


#Final Tkinter Display Build

# Creating root window
root = tk.Tk()


# Creating app display
app = LeafDetectorApp(root)


# Starting main loop
root.mainloop()
