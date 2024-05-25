# Investigating Misinformation: Analyzing Social Media to Identify Fake News

## Overview
This repository contains my finished research project on detecting fake news utilizing deep learning models such as LSTM, RNN, and BERT transformers. This research attempted to tackle the spread of misinformation on social media sites such as X (previously Twitter) by utilizing advanced natural language processing (NLP) techniques.

**NOTE**: The final paper can be found [here](./Deep%20Learning%20on%20Fake%20News%20Detection%20Final%20Paper.pdf).

### Key Achievements:
- **High Accuracy on News Datasets:** Achieved 90% accuracy with the RNN, 99% with LSTM, and 98% with BERT on structured news datasets.
- **Challenges with Social Media Content:** Identified the difficulty in adapting models to social media content, with approximately 50% accuracy on tweet datasets.
- **Sentiment Analysis:** Conducted sentiment analysis to explore the emotional tones of fake vs. real news, revealing that sentiment alone is not a reliable indicator of authenticity.

## Methodology
### Data Collection and Preprocessing:
- Collected over 40,000 labeled news articles and approximately 3,000 tweets.
- Preprocessed text data by normalizing, removing noise, and tokenizing.

### Model Development:
- **RNN and LSTM:** Utilized for their ability to handle sequential data.
- **BERT:** Leveraged for its advanced NLP capabilities and parallel processing.

### Evaluation Metrics:
- Evaluated models based on accuracy, precision, recall, and F1-score to ensure fairness and effectiveness.

## Results and Discussion
- **RNN:** Achieved 90% accuracy on news datasets but only around 50% accuracy on tweet datasets, highlighting challenges with shorter, informal text.
- **LSTM:** Achieved 99% accuracy on news datasets but similar struggles with tweets, performing at approximately 50%.
- **BERT:** Also performed exceptionally well on news datasets with 98% accuracy but faced similar issues with tweet data, achieving around 50% accuracy.
- Highlighted the need for further research to improve model performance on short, informal social media texts.
- Suggested hybrid approaches combining human oversight with AI for better misinformation detection.

## Future Work
- Explore advanced text analysis techniques for better handling of social media content.
- Investigate the use of transfer learning and multimodal data training to improve model generalization.

## Repository Contents
- **Code:** Implementations of RNN, LSTM, and BERT models.
- **Datasets:** Training and testing datasets used in the project.
- **Reports:** Detailed analysis and findings in PDF format.
- **Notebooks:** Jupyter notebooks with step-by-step code and explanations.

## Conclusion
This research contributes to the ongoing efforts to combat misinformation by providing insights into the effectiveness of various deep learning models. The findings emphasize the need for continuous improvement in AI techniques to adapt to the evolving nature of social media content.
