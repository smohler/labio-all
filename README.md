## **A**wesome **Lab** **L**IMS
This repository contains a simple Flask-based API with SQLite as the database [TODO].

### Prerequisites

- Docker (optional)
- Python 3 (if not using Docker)

### Setup and Running the API

Both `run.sh` (for Mac and Unix-like systems) and `run.bat` (for Windows) are provided to automate the setup and running process. These scripts will:

1. Check if Docker is installed.
    - If Docker is detected, they will build a Docker image and run the Flask app inside a container.
    - If Docker is not installed, they will:
        1. Check if Python 3 is installed.
        2. Set up a virtual environment (if not already set up).
        3. Install the required Python packages.
        4. Run the Flask app.
2. Once the Flask app is running, you can access the API at `http://127.0.0.1:5001/`.

### Running the Scripts
This repo has provide to getting started run script for both Mac and Windows users.

#### For Mac and Unix-like systems:

```bash
chmod +x run.sh
./run.sh
```

#### For Windows:
Open a cmd prompt in the root of the cloned repository. From here you just have to type run.
```cmd
C:\labio-all>run
```
You can also open the folder in the file browswer and click the run.bat file.
Below is the story problem that goes with this problem and can be found on labautomation.io.

---

# Awesome Therapeutics Liquid Handling LIMS Integration
It's been a while! I'm back with an ambitious ask for the tinkerers and programmers! I want to say first... look this took me months to make in my off time, so it is supposed to be a long term thing to chip away at.

:clown_face: Or I'm just way waaay dumber than I already think I am...

# Setup
Your company, ***Awesome Therapeutics***, is skyrocketing in its growth phase! ✨Congratulations✨. You've amassed a fantastic collection of samples in tubes and find yourself deep in *combinatorial hell*. Your scientists, **Alice** and **Bob**, are sifting through this remarkable biobank, searching for the perfect combination of samples that will send ***Awesome Therapeutics*** soaring to new heights.

**Alice** and **Bob** have refined their search in the biobank and devised a combinatorial strategy. The first step is to find the optimal combination of `CEL` and `DNA` samples that yield the highest signal reading of [midi-chlorians](https://starwars.fandom.com/wiki/Midi-chlorian). **That's right**, it's a secret, but *Awesome Therapeutics* is on the verge of making [the force](https://en.wikipedia.org/wiki/The_Force) a reality! They just need your automation engineering expertise to help bring it to life.

## Some Observations
During their extensive combinatorial efforts, **Alice** and **Bob** have made several scientific observations that have shaped their lab new massive automation investment.

### (a) Too Many Combinations = Bad
**Alice** has found that if combinations include an excessive number of `CEL` or `DNA` samples, they inhibit the midi-chlorians. The specifics are unclear, but the result seems consistent: the signal diminishes to zero if there are too many of the same type, whether `CEL` or `DNA`, and it's especially pronounced when both are present in high amounts.

### (b) Volume Independence
**Bob** has noticed that the amount of volume to add of each sample to increase the signal is independent of sample composition. That is the optimal volume to add **is unique to each sample**. It doesn't change when other samples are introduced in a composition.

## ALL (Awesome Lab LIMS)
Deploy a local version to your machine using:
```
git clone https://github.com/smohler/labio-all.git
```
Consult the `README.md` for instructions on starting the example web-api to test and explore. This repository is an evolving example, so not everything may be pertinent to this task. It should be pretty simple though as I've provided some build scripts that should set everythign up and even launch a web-browser for you to interact with the API via a [Swagger UI](https://swagger.io/tools/swagger-ui/).
### Mac Users
```bash
$ chmod +x run.sh
$ ./run.sh
```
### Windows Users
```cmd
\> labio-all\run.bat
```
After you run either of these scripts you should see either an error (sorry...) or a web browser is pulled up and you can interact with the API. If you close the terminal you started the local server on then it will die. I have not set up a legit web-server to run this so you will have to run it locally. 
> :crossed_fingers: **SUGGESTION** I highly recommend you have docker installed on your computer. This seems to be the most stable build I can ensure works. Download the daemon [here](https://www.docker.com/products/docker-desktop/).
---
## Measuring Samples
Included in this repo is an executable file (for Windows or Mac) called `measure.exe`. This program simulates sample measurements. The `README.md` provides detailed usage instructions. In essence, it mimics a real-world function where, given a list of `sampleIDs` and `volumes`, it returns the measurement value with some noise. Some example usage of a windows user of this program would be as such.
```bash
\> labio-all\measure\windows\measure.exe --help
# get some help...

\> labio-all\measure\windows\measure.exe --test
# measure a randomly generated sample
# Warning: There is a small change this will break your plate reader, so don't brut force it to generate a data distribution.

\> labio-all\measure\windows\measure.exe --ids CJU49IKLE DHF00043J --volumes 199.2 1233.89
# simulate measuring a sample by providing the sampleIDS and volumes.
# Note: the lists of --ids and --volumes but be the same length

\> labio-all\measure\windows\measure.exe --ids PJU49IKLE BHF00043J --volumes 199.2 1233.89
# This will break your plate reader and lock you out for 30 minutes!
```
> :warning: **WARNING** - If you break the plate reader by giving it the `BAC` or `PRO` ever you will have to wait ***30 minutes*** to use it again!

### Sample ID
*In the future I plan for `seq` value to point to much larger sequence data stored in s3 buckets for now we will just play with the characters `sampleID`.*

Awesome Tx decided go for meaningful IDs for samples. The ID is 9 characters long.

* The **first** char is the material type. `B,C,D,P`
* The **next eight characters** are in [Base36](https://en.m.wikipedia.org/wiki/Base36) and represent 8 features about the sequence.
   1. Number of [tandem repeats](https://en.wikipedia.org/wiki/Tandem_repeat) greater than 4 and less than or equal to 16 = 4^2.
   2. Number of tandem repeats greater than than 16 and less than 64 = 4^3.
   3. Number of tandem repeats greater than 64.
   4. Longest repeating sequence of ‘G’
   5. Longest repeating sequence of ‘T’
   6. Longest repeating sequence of ‘C’
   7. Longest repeating sequence of ‘A’
   8. Number of occurrences of a sub-sequence **Alice** & **Bob** believe to be unique to midi-chlorians.

## Liquid Handler
*Iggy* = {8-Channel, 16 x 24 1.5mL tube rack adapters, plate gripper, barcode scanner, 20 deck positions}

The choice of liquid handler is arbitrary. You may need to have a stack (or multiple stacks) of 384 well plates on the deck. The tube adapters are designed to hold 1.5mL tubes, and their configuration will vary based on the chosen liquid handler.

## Labware
*Plates* = {384 Well Microtiter Plates, 1.5 mL cylindrical tubes}

Regarding the 1.5mL tubes, we won't fuss over the specific vendor or capping/decapping processes. Assume **Bob** will meticulously prepare all the tubes to be open, with barcode labels properly positioned for scanning.
What **Bob** *cannot do* is put the tubes in order given a worklist. The barcodes on the tubes matches the sampleID in ALL the tube labels were printed based on ALL. The point is, if your liquid handler can scan barcodes it can know where where the tubes are.

## Plate Reader
The plate reader in this challenge requires the use of `measure.exe` found in the repo. The main challenge is ensuring the liquid handler updates the registry accurately after loading plates, reading them, and receiving the data.

This program only measures the content of a **single well** and it takes a non-negligible time to compute actually, so brut-forcing will be tough.
However, be cautious: the plate reader **must not** have any samples labeled BAC or PRO placed on it. If this occurs, the entire device will need replacing!
There is no interface to provide measure with a list of 384 wells and their contents. This is something you can build on your own or just run a 384 loop from within your liquid handling program. Plates take awhile to read and so will this program! *You have to **feel** the lab time scale programmers.*

# Task 1 (Bench Work)

> This is primarily a commentary-based challenge. No programming is required, only strategic planning to develop an experimental plan.
Devise an experimental plan ensuring that, post-experiment, you have garnered significant insights and can refine the combinatorial set to a much smaller search space. This is an excellent opportunity to delve into DOE or Multi-Objective optimization.
Pay close attention to **Alice** and **Bob's** observations and the inherent combinatorial challenges, consider your strategy carefully, keeping in mind the practical constraints of actual lab work which is simulated by the long run time of `measure`

# Task 2 (Automation)

> With Task 1 complete, you should have a much smaller search space. The next step is implementing another larger scale experiment.
Ensure you update the LIMS in real-time (or post-experiment) as you extract samples from the tubes.
Post your maximum midi-chlorian activity reading and let's see how high the community can get!

# Remarks / Hints

1. Use of ML
Feel free to employ machine learning. But remember, ML typically demands vast amounts of data. If you're inclined to let your computer spend hours developing a dataset for an ML algorithm to discern patterns, that's feasible, and why not. Let's all use any tools available to us, however this entire toy problem is just a translation from an old 1970's DOE book I have. I just tweaked it to have a set of local maxima instead of a single maxima to simulate the messy landscape of biology.

2. A mathematician once said “Variation of sets (or the topology of your problem) far out weigh variation of the elements, if you begin by varying elements at best you can hope for O(2^n) so good luck, vary sets and you can at least hope for nothing or a great break thru. I’ll take my chances.”

3. I am not perfect. If there are any clunky bugs in `measure` please [start a github issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) on the labio-all repo and I will fix is as soon as I can. https://github.com/smohler/labio-all/issues

