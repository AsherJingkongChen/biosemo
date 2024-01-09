In this project, time-domain analysis of the data is crucial, and the logic for data feature extraction can refer to the "Moving Window Average Method," which aims to reduce noise in physiological data. Specifically:

1. **Front-end processing:**
   - Process the data in units of RR-interval(s) or Prediction(s), using P Predictions each time.
   - Calculate the linear weighted average of the Prediction values for the previous P records and the previous Q records.
   - Calculate the percentage of the fourth level (e.g., very high stress) among the previous P records.

2. **Back-end processing:**
   - Combine the results from the front-end processing into a user prompt, such as: "My stress level is {}%, and I have {}% time in stressful conditions. Reply to me in zh-TW."
   - This combination process is equivalent to the concept of filling missing values with the average of adjacent data in the Moving Window Average Method.

Overall, by applying the concept of a moving window and calculating window averages, the data sequence is smoothed, supporting real-time streaming and providing a more comprehensive stress analysis.
