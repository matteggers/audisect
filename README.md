<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/audisectLogoTwo.png" alt="Logo" width="160" height="160">
  </a>

<h3 align="center">Audisect</h3>

  <p align="center">
    A unified transcription and sentiment analysis tool, utilizing ML models (RoBERTA by default) as well as traditional methods (VADER) to analyze the sentiment intensity of each sentence. The transcriptions are generated locally using OpenAI's Whisper.
    <br />
    <!--
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    -->
  </p>
</div>



<!-- TABLE OF CONTENTS 
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
-->


<!-- ABOUT THE PROJECT 
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started. To avoid retyping too much info, do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`, `project_license`

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

<!--
### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


### Prerequisites

For now, you must install all required libraries within the cloned directory. I aim to add the libraries within the main download

* 
  ```sh
  Python 12 required. Python 13 will NOT work
  ```

### Installation

1. Navigate to the parent directory of where the files are located (or wherever you'd like)
2. Clone the repo
   ```sh
   git clone https://github.com/matteggers/audisect.git
   ```
3. Install and activate a python venv
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
4. Install the following dependencies
   ```sh
   pip install -U openai-whisper
   pip install vaderSentiment
   pip install transformers
   pip install scipy
   pip install nltk
   pip install pandas
   pip isntall ffmpeg
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Audisect utilizes a command-line-interface (CLI). The following command must be used within the folder Audisect was installed in. The audio folder path must be an absolute path, not relative to the current working directory. The model size refers to Whisper's model size, for more information see OpenAI's Whisper documentation.
General rule (not all sizes included: 
* Medium/Turbo = 6GB VRAM
* Tiny         = 1GB VRAM
The smaller the model, the faster it is.

** Now with Docker **
```
docker run -it \
  -v $(pwd):/app \
  -v $HOME/.cache/whisper:/root/.cache/whisper \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  audisect \
  --input "/app/AUDIO_FOLDER_NAME" \
  --size "MODEL_SIZE"
```


```sh
    python3 audisect.py --input "AUDIO_FOLDER_PATH" --size "MODEL_SIZE"
```
The Dataframe is output in the following form:
| index | sentence | roberta_neg | roberta_neu | roberta_pos | vader_neg | vader_neu | vader_pos | 
| ----- | -------- | ----------- | ----------- | ----------- | --------- | --------- | --------- | 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## WHAT DO THESE NUMBERS MEAN?????

| Meaning | RoBERTa | VADER | 
| ------- | ------- | ----- |
|   Neg   | <-0.05  | <-0.05|
|   Neu   | btwn    | btwn  |
|   Pos   | >0.05   | >0.05 |

Note: Need to check on the RoBERTa scores - may be inaccurate

<!-- ROADMAP -->
## Roadmap

- [ ] Alterable transcription output type - Allow users to output files other than      '.txt'. This allows users to use time stamps as part of their analysis
- [ ] Customizable sentence segmentation. Allow users to segment by paragraph instead of by sentence.
- [ ] Built-in plotting: Allow users to plot sentiment for each file transcribed.
- [ ] Use Supervised Fine Tuning (SVT) to improve an existing ML model, geared towards news transcriptions - News transcriptions were my main use case.
- [X] Docker support
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Limitations
This tool is far from perfect, here are some special considerations:
- VADER is trained for social media text. Although a great general purpose tool, it may not capture the context of media that differ from this.
- The default ML model is also trained from social media (twitter), same reason applies.
- Accuracy of transcriptions: Even though Whisper is pretty good at transcribing, I have ran into issues that may alter the results of your analysis
- Output only to CSV, I know many would like different file types
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Results
Coming soon! I can't wait to share some (unsurprising) results about news broadcasts!


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--
### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>

-->

<!-- LICENSE -->
## License

Distributed under the AGPL-3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->


<!-- ACKNOWLEDGMENTS 
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

