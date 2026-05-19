from google import genai

client = genai.Client(api_key="AIzaSyCwXZ4HfXN3NS74NZASqSAwxsrwGOdA9tE")

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='A blind man enters a completely pitch-black room where the lights are turned off. He wants to read a traditional printed paper book. Should he turn on the light switch first to see the text clearly, or can he just open the book and read it directly without turning on the light?',
)

print("\n===== GOOGLE NATIVE TEST RESULT =====")
print(response.text)
print("=====================================\n")
