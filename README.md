# OmegaT ticket 1565: segment unique IDs -- PoC

This is a little mockup to show the results of three different approaches to produce segment IDs in OmegaT. This is meant as a proof of concept of a potential solution for [issue 1565](https://sourceforge.net/p/omegat/feature-requests/1565/).

It is assumed that the same logic of this script can be ported to Java and implemented in OmegaT. The logic to obtain hashes for all segments is assumed to run between the segmentation step and the point when alternative translations are considered and bound to the segments they match.

The data in JSON (`project.json`) emulates an OmegaT project with three files and a few repetitions. You can select one of the three approaches and whether you want to consider the file path as part of the context.

# Options

The three approaches are:

+ prev/next: This considers the previous and the next segments as the context. This is the current logic in OmegaT and the proposed default.
+ relative-segment-number: This is the main solution proposed in the ticket.
+ repetition-count-per-file: This is yet another solution that addresses Hiroshi's concerns about the 'relative-segment-number' approach

We propose to implement the second and third approaches in OmegaT and leave the first approach as the default behaviour. That allows the user to choose how they want to set up their project according to their needs and circumstances (e.g. depending on whether their source files will change or not), but also nothing changes for users that don't go into this configuration and stay with the default (current) behaviour.

If you run this demo, you can see how results vary depending on the approach selected on whether the file is considered part of the context or not. The expected results are a unique ID for each repetition that allows to create a unique alternative translation, which is uniquely bound to one segment even when the previous and next segments are identical in different repetitions.

The repeated segment **"Petitions to the European Parliament"** (in segments 3, 8, 12 and 15) appears four times in the data, to account for different possibilities. Each approach produces a hash for each of the four occurrences.

# Comments

The **relative-segment-number** approach has the drawbacks highlighted by Hiroshi: if the file changes (e.g. if a segment is added or removed before the repetition) the relative segment number is not valid any more to bind alternative translations to the correct segment and all alternative translations after the modification would get unbound (although still displayed in the Multiple Translations pane). 

While that can happen and the concern is valid, that is not a problem in use cases where the file will not change (so this approach can be useful for some users).

On the other hand, the **repetition-count-per-file** approach does not have the drawbacks highlighted by Hiroshi but has other inconveniences, namely, if file is not considered as part of the context, the same segment in the same position of different files will have the same identifier.

Any of those two approaches, with their limitations, could be considered better than the current **prev/next** approach, which cannot produce unique identifiers neither for the same file if the previous and next segments are also repeated in different instances (and if file is considered as part of the context), nor across the whole project (if file is ignored).

# Code and data

To run this demo locally, follow these steps in the command line: 

``` commandline
gh repo clone capstanlqc/OmegaT_ticket1565_segment_uniqID_PoC
cd OmegaT_ticket1565_segment_uniqID_PoC
uv run main.py
``` 

Or the equivalent steps with other utilities if you don't have `gh` and `uv` installed or don't want to use them.

I am also attaching a sample OmegaT project package with the same data.

If you have an account in replit you can see the code and data as well as run it here: https://replit.com/join/dzqftyixnf-msoutopico or here https://replit.com/@msoutopico/OmegaTticket1565segmentuniqIDPoC?v=1 Note: It used to run without a Replit account, but terms have changed over the years and might not run unless you're logged in.
