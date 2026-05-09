# REFLECTION.md
**Akinbobola Akinpelu | ITAI2376 | Solo Project**

---

## What Worked Well

Honestly, one of the things I was most proud of was getting the debugging workflow in VS Code to actually click for me. At first it felt like every error was a wall, but once I got comfortable reading the tracebacks and tracing issues back to their source, debugging started feeling less like a problem and more like part of the process.

The other big win was how the agents handled their responsibilities. Each agent — the Stock Analyst and the Trading Advisor — stayed in its lane. The Analyst pulled the live data and news, the Advisor interpreted it and gave a recommendation, and the handoff between them just worked. Seeing that workflow come together the way I designed it was genuinely satisfying. It felt like the system had a mind of its own, even though I knew exactly how it was structured under the hood.

---

## What Did Not Work and How I Handled It

The biggest early struggle was getting Git set up on Windows. Git wasn't installed, the terminal didn't recognize it, and I kept hitting errors like `fatal: repository not found` because I was using placeholder URLs instead of my actual repo link. It was a lot of small things stacking up at once.

I handled it by slowing down and going step by step — installed Git, restarted VS Code so it could register the new installation, and worked through the push commands one at a time. The `--allow-unrelated-histories` flag was one I'd never used before, but it solved the merge conflict between my local files and the GitHub-generated `.gitignore`.

I also want to be transparent about the scope of what I was able to complete. The original blueprint included features like ChromaDB for retrieval-augmented generation, a more robust execution layer for trade signals, and a few other components I had planned from the start. I wasn't able to get to all of it — and the honest reason is that I ended up going solo on this project. Managing the full system design, implementation, debugging, and documentation on my own within the time we had meant I had to make cuts. I prioritized getting a fully functional, working multi-agent system over stretching thin trying to hit every feature on the blueprint.

For ChromaDB specifically, I swapped it out for real-time tool calls using yfinance. For a trading system, live data actually makes more sense than a static knowledge base anyway — but I want to be clear that the decision was also partly driven by the time constraints of working alone.

---

## The Biggest Technical Challenge and How I Solved It

The hardest part was understanding how to wire up the CrewAI framework so the agents could actually communicate and pass information between each other. It's not just about writing two separate Python functions — you have to define the agents, assign them tools, set up the tasks in the right order, and make sure the output of one becomes the context for the next.

I got through it by reading the CrewAI docs carefully and testing incrementally. Instead of trying to run the whole crew at once, I made sure each individual piece worked before connecting them. Once I understood that tasks in CrewAI flow sequentially and that `context` is how agents share what they know, it all started making sense.

---

## Why I Chose Multi-Agent Over Single Agent

I could have kept it simple and built a single agent — and I probably would have gotten the hang of it eventually. But honestly, I wanted to push myself. I was curious about what it actually looks like when multiple agents have to coordinate with each other. What does it mean for one agent to "hand off" to another? How does the system stay coherent when different agents have different roles?

Going multi-agent was the harder path, but it taught me more. I came out of this project with a real understanding of how agent communication works, not just how to prompt a model. That felt worth the extra challenge.

---

## What I Would Build Next

If I had another semester, I'd add two things:

**ChromaDB** — I'd bring back the original RAG plan and build a knowledge base that the agents can query. Instead of only pulling live data, the system could also reference historical context, past analyses, or curated financial research. That combination of stored knowledge and real-time data would make the recommendations a lot more nuanced.

**A UI** — Right now everything runs in the terminal, which works but isn't exactly user-friendly. I'd build a simple web interface where someone could type in a ticker, see