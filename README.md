# Get Current Senate Member & Committee Assignments from authoritative data source

Authoritative data source: https://www.senate.gov/general/committee_assignments/assignments.htm#

### Workflow takes ~12 seconds from start to finish 
![](https://github.com/daeberly/Get-Clean-Current-Senate-Member-Committee-Info/blob/main/workflow_start_to_finish.JPG)
*Figure 1. Overall process using PowerAutomate for data acquisition and Python for manipulation.*

## Purpose
This workflow pulls authoritative data from senate.gov on current members in the Senate to include their committee assignment, public website, political party and state. 

### It includes two parts: 
- (1) power automate workflow that gets raw data into a .csv [run time: ~11 seconds] <br />
- (2) a python script that cleans the data into a readable excel table [run time: 0.4 seconds].

#### Step 1: Power Automate Desktop flow
![](https://github.com/daeberly/Get-Clean-Current-Senate-Member-Committee-Info/blob/main/power_automate_flow.JPG)
*Figure 2. PowerAutomate Workflow.*

#### Step 2: Final Product
![](https://github.com/daeberly/Get-Clean-Current-Senate-Member-Committee-Info/blob/main/final.JPG)
*Figure 3. Cleaned excel table.*

### System requirements to run workflow:
- Windows "Power Automate"
- Microsoft Edge or any internet explorer
- Excel
- Python installed (i.e. Spyder, Anaconda, etc.)

Note: Power Automate desktop flows are unable to be exported. Therefore, I have a screen shot of the flow & results when it is finished. The flow is 3 steps and easy to build once you know what steps to do and how to record your actions on the website. 

Example tutorial on how to scrape websites using Power Automate: "Web Scraping in Power Automate for Desktop (Full Tutorial)" https://www.youtube.com/watch?v=WXK0u2yXLrU&t=1