# WordCloud Generator

This project generates a word cloud visualization from a given text input. The word cloud highlights the most frequent words in the text, with their sizes proportional to their frequency.

## Features
- Generates a word cloud from text data.
- Supports stopwords to exclude common words.
- Customizable background color.
- Save the word cloud as an image file.
- Export the word cloud along with metadata (e.g., word frequencies) to a PDF report.
- Create animated word clouds that transition between different shapes or color schemes.
- Real-time word cloud updates with dynamic text data.

## Requirements
Make sure you have the following Python packages installed:
- `wordcloud`
- `matplotlib`
- `fpdf`

You can install the required packages using the following command:
```bash
pip install -r requirements.txt
```

## Usage
1. Provide your text data via a file using the `--input` argument:
```bash
python src/main.py --input path/to/your/textfile.txt
```
2. The word cloud will be displayed in a window.
3. The word cloud will be saved as an image file (`wordcloud_output.png`).
4. A PDF report (`wordcloud_report.pdf`) containing the word cloud and metadata will be generated.

## Example
```python
text = "Your text data goes here"
wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
```

## License
This project is licensed under the MIT License.