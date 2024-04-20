
# To Scrap and manipulate the data of the youtube captions
library(youtubecaption)  
# To make api request to the API
library(httr)
# For Parsing JSON Data
library(jsonlite)
# For string Manipulation
library(stringr)
# To Use Python Functionalities in R
library(reticulate)
# For data manipulation
library(dplyr)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           First part 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Youtube Data API key 
api_key <- "AIzaSyBGAKNJLkAm50rih2Fy65BkAheUK20PIh8"

# Search for videos with captions which has appropriate sentence structure
search_url <- paste0(
  "https://www.googleapis.com/youtube/v3/search",
  "?part=snippet",
  "&q=science",  # Replace with your search keywords
  "&maxResults=10",    # Adjust the number of results as needed
  "&type=video",
  "&videoCaption=closedCaption",
  "&key=", api_key
)

# Making Request
search_response <- GET(search_url)

# Fetching data from response
search_data <- content(search_response, "text")

# Parsing the JSON data
search_results <- fromJSON(search_data)

# Loop through search results and retrieve captions
video_id <- search_results[["items"]][["id"]][["videoId"]]

# Asking user to which video id to use for to fetch the youtube captions
# Prompt the user for input and store it in a character variable
user_input <- readline("Enter the Number Between 1 TO 20: ")

# Convert the user's input to an integer
which_id <- as.integer(user_input)

# Check if the conversion was successful
if (!is.na(which_id) && which_id >= 1 && which_id <= 20) {
  cat("You entered:", which_id, "\n")
} else {
  cat("Invalid input. Please enter a valid integer between 1 and 20.\n")
}

# Making video URL for fetching the actual captions
video_url <- paste0("https://www.youtube.com/watch?v=",video_id[which_id])
  
# get_captoins will fetch the captions of the provided video URL
  captions <- get_caption(video_url)
  
#Extracing the column which contain the caption sentence in data frame
column_caption = captions[,c(2)]
  
# Creating empty data variables
temp = ""
text = ""
  
# To remove All the white space character from the scrap caption
  for( i in column_caption)
  {
    temp <- gsub("\\\\", "", i)
    temp <- gsub("\n", " ", i)
    text = paste(text , temp , " ")
  }
  
# Another empty data variables
  caption_text = ""
  
# concatnating the each captions lines to form the Whole paragraph
  for(i in text)
  {
    caption_text = paste(caption_text , i , " ")
  }
  
# Removing extra white space from the paragraph of the captions
  cleaned_text <- gsub("\\s+", " ", caption_text)
  
# Extract sentences based on periods
  sentences <- unlist(str_extract_all(cleaned_text, "[^.]+\\."))
  
  # Check if the character vector is empty
  if (length(sentences) == 0) {
    sentences <- paste(cleaned_text, ".", sep = " ")
  } else {
    print("The character vector is not empty.")
  }
  
  
#how many rows in the data frame of caption
  rows = length(sentences)

# Showing the number of total sentence so user can select how many to select out of it wisely
  print(paste("The Number Of Total Sentence ",rows))
  
# Taking the number of sentece to be selected randomaly from the group of sentences
  user_input <- readline("Enter the Number sentece to be selected randomaly from the group of sentences : ")
  
  # Convert the user's input to an integer
  how_many <- as.integer(user_input)
  
  # Check if the conversion was successful
  if (!is.na(how_many) && how_many >= 1 && how_many <= rows) {
    cat("You entered:", how_many, "\n")
  } else {
    cat("Invalid input. Please enter a valid integer between 1 and ", rows ,".\n")
  }
  
  
# Diving the sentences into group of floor(rows/10) number of sentences  
  row = floor(rows/how_many)
  
# intializing count for the keeping track of segment
  count=0
  
# Path of the file where this sentence is to be store for the later use
  file_path = "D:/Ronak/Python/questions_text.txt"
  temprorary = ""
  counter_for_sentence = how_many
  
  while(counter_for_sentence>0){
    # Generating random number in the range og [1,row]
    TenRandomNumbers <- sort(sample.int(row, 1))
    print(TenRandomNumbers)
    # Adding new line character at the end the distinguish the sentences
    temprorary = paste(sentences[count+TenRandomNumbers],"\n")
    # Storing the randomly selected sentece into the specified path
    cat(temprorary, file = file_path, append = TRUE)
    print(sentences[count+TenRandomNumbers])
    count=count+row
    counter_for_sentence = counter_for_sentence - 1
  }

  

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           Second part 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  
  

# Selecting which Python enviroment to use with reticulate
  use_python("C:/Users/DC/anaconda3/python.exe")
# Checking if whether the python is configure to our R Session or not
  reticulate::py_config()
# Check if python is available (For the Surity)
  reticulate::py_available()
  
# # this package are alredy install into the current python virtual enviroment /
#   
# # Install Python package into virtual environment
#   reticulate::py_install("transformers", pip = TRUE)
#   
# # Also installing pytorch just as a contingency?
#   reticulate::py_install(c("torch", "sentencepiece"), pip = TRUE)
#   
 
  # Importing ???? transformers into R session
  transformers <- reticulate::import("transformers")

  # Using "question-answering" model of the transformers 
  reader <- transformers$pipeline(task = "question-answering")
  
  
  # Reading the Question Generated by the python call from a "question.txt" file
  lines_form_questions <- readLines("D:/Ronak/Python/question.txt")
  
  # Reading the sentence that are produce by the R code above
  lines_from_sentence <- readLines("D:/Ronak/Python/questions_text.txt")
  
  # looping through sentence and questions 
  
  for(i in 1:how_many){
    sentencesss = lines_from_sentence[i]
    questions = lines_form_questions[i]
    
    print(lines_from_sentence[i])
    print(lines_form_questions[i])

    # Provide model with question and context
    outputs <- reader(question = questions, context = sentencesss)
    outputs %>% 
      as_tibble()
    
    print(outputs[4])
  }

  
  
  
  
  

 