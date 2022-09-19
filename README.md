# OmegaT ticket 1565: segment unique IDs -- PoC

I have created a little mockup in Python to show the results of three different approaches to produce segment IDs in OmegaT. This meant as a proof of concept of potential solutions for [issue 1565](https://sourceforge.net/p/omegat/feature-requests/1565/).

I am assuming that whatever runs in Python with this data can also run in Java in OmegaT.

The data emulates an OmegaT project with three files and a few repetitions. You can select one of the three approaches and whether you want to consider the file path as part of the context.

# Options

The three approaches are:

+ prev/next: This considers the previous and the next segments as the context. This is the current logic in OmegaT and the proposed default.
+ relative-segment-number: This is the solution proposed in this ticket.
+ repetition-count-per-file: This is yet another solution that addresses Hiroshi's concerns about the 'relative-segment-number' approach

My proposal is to implement the second and third approaches in OmegaT and leave the first approach as the default. That allows the user to choose how they want to set up the project according to their needs and circumstances (e.g. depending on whether their source files will change or not), but also nothing changes for users that don't go into this configuration and stay with the default (current) behaviour.

# Comments

The **relative-segment-number** approach has the drawbacks highlighted by Hiroshi: if the file changes (e.g. if a segment is added or removed before the repetition) the relative segment number is not valid any more to bind alternative translations to the correct segment and all alternative translations after the modification would get unbound (although still displayed in the Multiple Translations pane).

The **repetition-count-per-file** approach does not have the drawbacks highlighted by Hiroshi but has other inconveniences, namely, if file is not considered as part of the context, the same segment in the same position of different files will have the same identifier.

Any of those two approaches, with their limitations, could be considered better than the current **prev/next** approach, which cannot produce unique identifiers neither for the same file if the previous and next segments are also repeated in different instances (and if file is considered as part of the context), nor across the whole project (if file is ignored).

# Code and data

If you have an account in replit you can see the code and data as well as run it here: https://replit.com/join/dzqftyixnf-msoutopico

Otherwise you can just run it here: https://replit.com/@msoutopico/OmegaTticket1565segmentuniqIDPoC?v=1

If you prefer, you can clone the data and code from https://github.com/capstanlqc/OmegaT_ticket1565_segment_uniqID_PoC

I am also attaching a sample OmegaT project package with the same data.
