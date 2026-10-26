# Interview answers for the Overseer and Routing cover letters

Gathered 24 September 2026, one question at a time. Manit's own words, recorded verbatim.

**Q1. Has Claude or Claude Code ever given you an answer that sounded confident but was wrong?**
> Claude hasnt for quite a while, but chatgpt has. It really depends on how u use the tool and the context and how u save it. In recent times it hasnt no.

Note: "depends on the context and how you save it" links straight to Routing's objective 2 (extract context from a task request).

**Q2. What do you actually do to give Claude good context?**
> I make sure to use folders and save important facts in claude.md. Using folders and having files in one place is better than using it in web. Because it can directly read the folder and all files in it. I also organize the folders and files and make sure to use that to do things. So it can look at certain folders for certain tasks

Note: he routes tasks to context by hand (certain folders for certain tasks). Routing's brief is about doing that automatically.

**Q3. Do you ever pick a different model or mode depending on the task?**
> No, always the strongest

Note: he is the user their brief describes, using the big model for everything. Curiosity angle: how much of what he asks could a smaller model have handled, and how would a system know?

**Q4. Why do you always use the strongest model?**
> I never run outta credits even on higher model.

Note: cost never forced the choice on him as an individual. The letter can be curious about what changes at scale, where a multi-agent system runs thousands of requests and cost does bite.

**Q5. Has a task that looked simple ever turned out much harder than expected?**
> Yes, in my own project

**Q6. Which one was it?**
> Both adding the rollback to the backend logic and the robot resetting(brownout)

Note: both are "looked simple, was not" stories. Rollback: undoing by workflow looked right but position is cumulative, so it had to become LIFO. Brownout: resets looked like a code bug, turned out to be power, proved via bootId/resetCause telemetry. Matches Routing's "more complex than they initially appear".

**Q7. When Claude writes code for you, how do you check it's actually correct?**
> Kinda trust it blindly. If its backend work or coding logic, I read through the logic, see if it works as intended. I also use debugger. But mostly I just trust blindly. I focus on making the logic work rather than if its 100 percent correct. Kinda brut force approach

Note: honest, and usable for Overseer if framed well: for his own code "seems to work" is good enough, but a factory cannot run on "seems to work". That contrast is the curiosity. Do not print "trust blindly" in the letter as is.

**Q8. Any connection to factories or manufacturing at all?**
> Only through my robot

**Q9. What are you most curious about in the Overseer project?**
> What is the right answer, whats the judgement. How catch it getting worse aswell. Both.

**Q10. What are you most curious about in the Routing project?**
> How does it know it's unsure?
