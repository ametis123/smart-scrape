# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 Opentensor Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import re
import random


class BasePrompt:
    r"""Base class for prompts expecting an extractable response."""

    def __init__(self):
        self.template = ""
        self.extract_pattern = ""

    def text(self, *args) -> str:
        r"""Sanitize input strings and format prompt template."""
        sanitized = args
        tags = find_unique_tags(self.template)
        for tag in tags:
            sanitized = [arg.replace(tag, "") for arg in sanitized]

        return self.template.format(*sanitized)

    def extract(self, response: str):
        r"""Search for the extract pattern in the text using regex."""
        result_pattern = re.compile(self.extract_pattern, re.DOTALL)
        result = re.findall(result_pattern, response)

        # If result found, return it.
        if result:
            return result[0]

        # If no result found, return None.
        return None

    def matches_template(self, input_text) -> bool:
        r"""Checks if the input_text matches the first unformatted part of the prompt template."""
        index = self.template.find("{")
        return input_text[:index] == self.template[:index]

class ScoringPrompt(BasePrompt):
    def __init__(self):
        super().__init__()
        self.extract_pattern = r"\b([0-9]|10)\b"

    def extract_score(self, response: str) -> float:
        r"""Extract numeric score (range 0-10) from prompt response."""
        extraction = self.extract(response)
        if extraction is not None:
            try:
                score = float(extraction)
                if 0 <= score <= 10:
                    return score
            except ValueError:
                return 0
        return 0

    @staticmethod
    def mock_response():
        r"""Mock responses to a followup prompt, for use in MockDendritePool."""
        return random.choices(
            ["", f"{ random.randint(0, 10) }</Score>"], weights=[1, 9]
        )[0]


class SummaryRelevancePrompt(ScoringPrompt):
    r"""Scores a summary on a scale from 0 to 10, given a context."""

    def __init__(self):
        super().__init__()
        self.template = summary_relevance_scoring_template

class LinkContentPrompt(ScoringPrompt):
    r"""Scores a summary on a scale from 0 to 10, given a context."""

    def __init__(self):
        super().__init__()
        self.template = link_content_relevance_template

def find_unique_tags(input_text: str):
    r"""Find all substrings that match the pattern '<...>'."""
    matches = re.findall("<([^>]*)>", input_text)
    # Return a list of unique matches.
    return list(set(matches))

summary_relevance_scoring_template = """
Evaluate the correctness, relevance, and depth of an answer given a context and question, focusing on the inclusion of Twitter links as supporting evidence. 
Scores range from 0 to 10:
- 0 for answers completely unrelated or incorrect, especially those not addressing the question's topic.
- 2 for answers relevant to the question but lacking any Twitter links as evidence.
- 3-9 for answers that vary in correctness, relevance, and the inclusion of Twitter links, with higher scores reflecting better quality and more relevant evidence.
- 10 for answers that are not only accurate and relevant but also well-supported by Twitter links, fully addressing the question's demands.

Score Examples:
- Score 0: Answer discusses a completely different topic without any relation to the question.
- Score 2: Answer is on topic but does not provide any Twitter links to support its statements.
- Score 6: Provides a partially correct response with some Twitter links, but lacks comprehensive coverage or depth on the topic.
- Score 8: Offers a thorough answer with relevant Twitter links but misses minor details or broader implications.
- Score 10: Fully satisfies the question with accurate, relevant information and substantial evidence from Twitter links.

Additional Scoring Criteria:
- Accuracy and relevance to the question.
- Depth of insight and coverage of the topic.
- Presence and relevance of Twitter links as supporting evidence.

Example for Score 2:
<Question>
What are the latest innovations in electric vehicles according to Twitter discussions?
</Question>

<Answer>
Electric vehicles are seeing major advancements in battery technology and charging infrastructure, improving range and reducing charging times. However, no specific Twitter links are provided to support these claims.
</Answer>

<Score>2</Score>
Explanation: The answer is relevant but lacks Twitter links as evidence, thus earning a score of 2.

Example for Score 6:
<Question>
How is Twitter influencing political campaigns?
</Question>

<Answer>
Twitter significantly influences political campaigns by allowing direct communication between candidates and voters. Some examples include general observations of increased engagement rates, but specific influential tweets or campaigns are not cited.
- [General observation by @PoliticsToday](https://twitter.com/PoliticsToday/status/1234567890)
</Answer>

<Score>6</Score>
Explanation: The answer includes a Twitter link and covers the topic, yet it lacks depth and specific examples of influence, meriting a score of 6.

Example for Score 8:
<Question>
What are the key challenges facing remote work as shared on Twitter?
</Question>

<Answer>
Remote work challenges include maintaining productivity and managing team communication. Key discussions on Twitter highlight solutions and strategies:
- [Tweet by @RemoteWorkInsider](https://twitter.com/RemoteWorkInsider/status/1234567890) on communication tools.
- [Tweet by @ProductivityGuru](https://twitter.com/ProductivityGuru/status/0987654321) discussing time management techniques.
However, the answer does not address issues like cybersecurity and employee well-being.
</Answer>

<Score>8</Score>
Explanation: The answer provides relevant Twitter links and addresses key challenges but lacks completeness, scoring an 8.

Remember, the inclusion and relevance of Twitter links are essential for higher scores, as they serve as concrete evidence that strengthens the answer's credibility and depth.

<Question>
{}
</Question>

<Answer>
{}
</Answer>

<Score>"""


link_content_relevance_template = """
Evaluate the relevance of the content from Twitter links provided in <LinksContent></LinksContent> to the question or statement in <Prompt></Prompt>. Assign a score between 0 and 10 in <Score></Score> tags. A score of 0 indicates no relevance, while a score of 10 signifies perfect relevance.

Scoring Guidelines:
- 0: No relevance between Twitter content and the prompt.
- 2: Minimal relevance; the content barely relates to the prompt.
- 6: Moderate relevance; the content relates to the prompt but misses key aspects or details.
- 8: High relevance; the content is closely related to the prompt, with minor details lacking.
- 10: Perfect relevance; the Twitter content directly addresses the prompt comprehensively.

Scoring should be based on the directness of the relevance and the completeness of the Twitter content in addressing the prompt's topic. 

Examples:

<Prompt>
Impact of social media on public opinion.
</Prompt>

<LinksContent>
Tweets discussing studies on social media's influence on political decisions.
</LinksContent>

<Score>8</Score>
Explanation: The content is highly relevant to the prompt, focusing on a specific aspect (political decisions) of the broader topic.

<Prompt>
Advancements in renewable energy.
</Prompt>

<LinksContent>
Tweets about recent solar power breakthroughs and wind energy projects.
</LinksContent>

<Score>10</Score>
Explanation: The Twitter content perfectly matches the prompt, covering advancements in renewable energy directly.

<Prompt>
Trends in global travel.
</Prompt>

<LinksContent>
Tweets primarily discussing new tech gadgets.
</LinksContent>

<Score>0</Score>
Explanation: The content of the tweets is unrelated to the prompt's focus on global travel, showing no relevance.

Maintain objectivity and focus solely on the relevance of the Twitter link content to the prompt for accurate scoring.

<Prompt>
{}
</Prompt>

<LinksContent>
{}
</LinksContent>

<Score>"""