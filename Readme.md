Differential privacy
You have a bunch of private numbers (for example, people’s ages) and you want to share just the average age without letting anyone figure out exactly what any one person’s age is.


Basic Idea: Add a Little “Fuzz”
Instead of publishing the exact average, we add a small random error (we call it “noise”) so that the number you see isn’t exactly the real average—but it’s still very close.

If the true average is 35, we might add noise of +1.2 or –0.7, and publish 36.2 or 34.3 instead.

The noise is drawn from a special distribution (called Laplace) that’s centered at zero, so on average we don’t shift the result, but individual outputs vary.




We pick a “privacy budget” denoted ε (epsilon):

Small ε (e.g. 0.1) ⇒ lots of noise, more privacy, less accurate average.

Large ε (e.g. 1.0) ⇒ little noise, less privacy, more accurate average.

That lets you choose how much you’re willing to trade accuracy for privacy.
