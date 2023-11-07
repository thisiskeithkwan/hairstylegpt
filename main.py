import openai
import streamlit as st
import base64
import requests
import json


openai_api_key = st.secrets['openai']["OPENAI_API_KEY"]

prompt = '''anaylze the person's facial and hairstyle characteristics using the following format and return as json
                {
  "facial_features": {
    "face_shape": "",
    "forehead": {
      "width": "",
      "height": ""
    },
    "eyebrows": {
      "shape": "",
      "thickness": ""
    },
    "eyes": {
      "size": "",
      "set": ""
    },
    "nose": {
      "length": "",
      "width": ""
    },
    "cheekbones": {
      "position": "",
      "pronounced": ""
    },
    "jawline": {
      "strength": "",
      "angle": ""
    },
    "chin": {
      "type": "",
      "shape": ""
    }
  },
  "hairstyle": {
    "length": "",
    "texture": "",
    "volume": "",
    "style": "",
    "parting": "",
    "bangs": {
      "present": false,
      "style": ""
    },
    "color": "",
    "thickness": ""
  },
  "Hairstyle Match analysis": "a 30 words analysis of matchness of haircut and facial characteristic",
  "Match Score": "an int of 0-100"
  "Recommendations for current haircut": "",
  "Other Hair styles to consider": "briefly describe 3 haircuts that might suit the client and why"
}


Return nothing but a valid json that can be correctly parsed by python'''

def display_analysis(response_data):
    try:
        # Access the relevant data from the response JSON
        content_json = json.loads(response_data['choices'][0]['message']['content'].strip('```json\n'))
        
        # Extract the relevant information
        match_score = content_json.get('Match Score', 'No score provided.')
        hairstyle_match_analysis = content_json.get('Hairstyle Match analysis', 'No analysis provided.')
        current_haircut_recommendations = content_json.get('Recommendations for current haircut', 'No recommendations provided.')
        other_hairstyles = content_json.get('Other Hair styles to consider', 'No other hairstyles provided.')
        
        # Display the extracted information
        st.header('Analysis Results')

        st.subheader('Matching Score')
        st.metric(label="Score", value=match_score)
        
        st.subheader('Analysis')
        st.write(hairstyle_match_analysis)

        st.subheader('Recommendations for Current Haircut')
        st.write(current_haircut_recommendations)

        st.subheader('Other Hairstyles to Consider')
        # Assuming the 'Other Hair styles to consider' is a semicolon-separated string
        other_hairstyles_list = other_hairstyles.split(';')
        for hairstyle in other_hairstyles_list:
            st.write(f"- {hairstyle.strip()}")  # Strip to remove any leading/trailing whitespace
        
    except json.JSONDecodeError:
        st.error('There was an error decoding the JSON response.')
    except KeyError as e:
        st.error(f'Missing key in response data: {e}')
    except Exception as e:
        st.error(f'An error occurred: {e}')



# Function to encode the image
def encode_image(image_file):
    # Convert the file to read it into bytes
    img_bytes = image_file.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

# Streamlit app
def main():
    st.title('Hairstyle GPT')
    st.subheader("Rate your hairstyle accroding to your face")

    # User uploads an image from camera
    picture = st.camera_input("Take a picture")

    if picture:
        # Display the captured image
        #st.image(picture)

        # Encode the image to base64
        base64_image = encode_image(picture)

        # OpenAI API Key
        api_key = "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"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
            }


        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": prompt
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                  }
                ]
              }
            ],
            "max_tokens": 400
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            st.success("The image has been successfully analyzed!")
            response_data = response.json()
            #st.write(response_data)
            display_analysis(response_data)
        else:
            st.error("Failed to analyze the image.")


def display_footer(twitter_handle):
    twitter_url = f"https://twitter.com/{twitter_handle}"
    footer_html = f"""
    <div style='position: relative; margin-top: 20px; padding: 10px; text-align: center;'>
        <hr>
        <p>Made by <a href="{twitter_url}" target="_blank"> <img src='https://img.icons8.com/fluent/48/000000/twitter.png' /> @{twitter_handle}</a></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

        
# Run the Streamlit app
if __name__ == '__main__':
    main()
    display_footer('KeithKwan15')

