### Insurance-Adjuster-Voicemails

## Overview

This Tableau project serves as a demonstration of the kinds of claim quality insights that become available when voicemail transcription is available. The dataset was artificially generated to avoid using sensitive information. I used Anthropic's Claude AI to create a prompt to set parameters that would create an approximation of the volume and types of voicemails a typical non-injury adjuster might get. Claude generated a python script that I entered into a Google Colab notebook to generate an excel file with 745 voicemails running from July 1, 2024 to February 28, 2025.   

## To Do and Limitations

There are a few things outside of the scope of this project that will be necessary to build it from the ground up. There are also possible limitations.

 - The voicemail service will need a reliable transcription function to catalog claim numbers, caller names, shop or company names, and keywords.
 - The dataset includes categories created by the python script. In the real work environment, voicemails would come in without context. There would have to be an NLP or other ML process that provides a meaningful category for each voicemail.
 - For the best quality of data, the transcription and categorization would have to be automatic for all voicemails and stored on servers, representing a cost if scaled to every member service representative.

## Visualizations

I used Tableau Public to create visualizations showing a few of the insights possible with this dataset. Some of the insights beyond the charts above are:

 - Showing which keywords or shops appeared most frequently in the complaint category.
 - Identifying an abnormally large number of supplement requests in October and November.
 - Determining what voicemail category contained the most repeat callers.

## Conclusion

This is just a small portion of what may be possible. When combined with data such as what shop was used for repairs, customer satisfaction score, and year/make/model of vehicle, the feedback from voicemails could help develop a clearer picture of what tends to create the most issues within a claim. This would aid in developing targeted solutions for adjusters and other stakeholders to mitigate specific pain points for members, shops, and claimants.
