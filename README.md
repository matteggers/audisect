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

### Purpose

This tool was birthed out of curiosity regarding national news sentiment. Initially, this was supposed to find the most used word in a collection of NBC news broadcasts after I heard "chilling details" multiple days in a row. My family frequently watches cable news -\_-. I pivoted into finding sentiment as that would provide more insight into how this form of media may affect a person's emotional state.

### Prerequisites

- Ubuntu or WSL2
- Python 3.12
- Nvidia GPU
- CUDA PyTorch >= 2.6 wheel
- ffmpeg in PATH

### Installation

Clone: https://github.com/matteggers/audisect.git

```sh
cd audisect
python3 -m venv .venv
source .venv/bin/activate
sudo apt-get update && sudo apt-get install -y ffmpeg
pip install --upgrade --index-url https://download.pytorch.org/whl/cu121 "torch>= 2.6"

# Install Audisect
pip install -e .
```

#### Docker

Coming soon. Previously had issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Audisect is used through a CLI. The following are two supported methods for using audisect.

### Transcription Model Sizes - Directly from OpenAI's Whisper

There are six model sizes, four with English-only versions, offering speed and accuracy tradeoffs.
Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model.
The relative speeds below are measured by transcribing English speech on a A100, and the real-world speed may vary significantly depending on many factors including the language, the speaking speed, and the available hardware.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
| :----: | :--------: | :----------------: | :----------------: | :-----------: | :------------: |
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~10x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~7x       |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~4x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
| turbo  |   809 M    |        N/A         |      `turbo`       |     ~6 GB     |      ~8x       |

### Using custom Sentiment Analysis Models

1. Navigate to src/audisect/pipeline.py
2. In init, change contents of string to desired HuggingFace model.

### WSL

- Using Windows path style

```sh
audisect run \
 -i "$(wslpath -a -u 'C:\Users\<YOU>\<INPUT FOLDER PATH>')" \
  -o "$(wslpath -a -u 'C:\Users\<YOU>\<OUTPUT FOLDER PATH>')" \
 -s size
```

- Using WSL path style

```sh
audisect run \
  -i "/mnt/c/Users/<YOU>/Downloads/input_test" \
  -o "/mnt/c/Users/<YOU>/Downloads/output_test" \
  -s size
```

### Ubuntu

```sh
audisect run \
  -i "/home/<you>/input_test" \
  -o "/home/<you>/output_test" \
  -s size
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Output Structure

```text
output/
├─ csv/
│  └─ example.csv
└─ txt/
   └─ example.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Interpreting Sentiment Scores

The score for each is between -1 and 1. Any result between -0.05 and 0.05 is neutral, with results >0.05 being positive and opposite for negative sentiment.

| Meaning | RoBERTa | VADER  |
| ------- | ------- | ------ |
| Neg     | <-0.05  | <-0.05 |
| Neu     | btwn    | btwn   |
| Pos     | >0.05   | >0.05  |

<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- ROADMAP -->

## Roadmap

- [ ] Alterable transcription output type - Allow users to output files other than '.txt'. This allows users to use time stamps as part of their analysis
- [ ] Customizable sentence segmentation. Allow users to segment by paragraph instead of by sentence.
- [ ] Use Supervised Fine Tuning (SVT) to improve an existing ML model, geared towards news transcriptions - News transcriptions were my main use case.
- [ ] Docker support
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Limitations

This tool is far from perfect, here are some special considerations:

- VADER is trained for social media text. Although a great general purpose tool, it may not capture the context of media that differ from this.
- The default ML model is also trained from social media (twitter), same reason applies.
- Accuracy of transcriptions: Even though Whisper is pretty good at transcribing, I have ran into issues that may alter the results of your analysis
- Output only to CSV, I know many would like different file types
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Results

Currently processing large amounts of data on news broadcasts. Results coming soon.

<!-- CONTRIBUTING -->

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
