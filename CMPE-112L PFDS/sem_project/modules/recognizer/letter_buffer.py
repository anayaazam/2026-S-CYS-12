# Letter Buffering and Temporal Smoothing for SignBridge
from collections import Counter
from typing import List, Optional, Tuple

class LetterBuffer:
    """Implements temporal smoothing and character debouncing for ASL predictions.
    Ports window_extract and map_extract logic from Repo 1.
    """

    def __init__(self, window_size: int = 15, stability_threshold: int = 10) -> None:
        self.window: List[str] = []
        self.window_size = window_size
        self.stability_threshold = stability_threshold
        self.sentence_buffer: List[str] = []
        self.last_stable_letter: Optional[str] = None
        self.consecutive_empty = 0

    def add_prediction(self, letter: Optional[str]) -> Tuple[Optional[str], bool]:
        """Adds a raw prediction to the sliding window.
        Returns a tuple of (stable_letter, is_new_letter).
        """
        if not letter:
            # If no hand is detected, we slowly clear the window
            self.consecutive_empty += 1
            if self.consecutive_empty > 5 and self.window:
                self.window.pop(0)
            return None, False

        self.consecutive_empty = 0
        self.window.append(letter)
        if len(self.window) > self.window_size:
            self.window.pop(0)

        # Execute window_extract equivalent
        stable_letter = self.window_extract(self.window_size)
        
        is_new_letter = False
        if stable_letter and stable_letter != self.last_stable_letter:
            self.last_stable_letter = stable_letter
            is_new_letter = True
            self.map_extract(stable_letter)
            
        return stable_letter, is_new_letter

    def window_extract(self, size: int = 15) -> Optional[str]:
        """Extracts the most frequent letter in the sliding window if it meets
        the stability threshold.
        """
        if len(self.window) < self.stability_threshold:
            return None

        counter = Counter(self.window)
        most_common, count = counter.most_common(1)[0]
        
        if count >= self.stability_threshold:
            return most_common
        return None

    def map_extract(self, letter: str, limit: int = 4) -> None:
        """Appends the letter to the sentence buffer, ensuring we debounce duplicates
        and don't exceed reasonable consecutive repetitions (e.g. limit=4).
        """
        # If the sentence buffer is empty, just append
        if not self.sentence_buffer:
            self.sentence_buffer.append(letter)
            return

        # Check consecutive repetitions of the same letter
        last_letter = self.sentence_buffer[-1]
        if letter == last_letter:
            # Count how many of this letter are consecutive at the end of the buffer
            consec_count = 0
            for char in reversed(self.sentence_buffer):
                if char == letter:
                    consec_count += 1
                else:
                    break
            
            # Only append if we haven't reached the repetition limit
            if consec_count < limit:
                self.sentence_buffer.append(letter)
        else:
            self.sentence_buffer.append(letter)

    def add_space(self) -> None:
        """Appends a space to the sentence buffer to separate words."""
        if self.sentence_buffer and self.sentence_buffer[-1] != " ":
            self.sentence_buffer.append(" ")
            self.last_stable_letter = None # Reset so they can sign the same letter in a new word

    def backspace(self) -> None:
        """Removes the last character from the sentence buffer."""
        if self.sentence_buffer:
            self.sentence_buffer.pop()
            self.last_stable_letter = None

    def clear(self) -> None:
        """Clears the buffer."""
        self.window.clear()
        self.sentence_buffer.clear()
        self.last_stable_letter = None

    def get_sentence(self) -> str:
        """Returns the accumulated sentence as a string."""
        return "".join(self.sentence_buffer)
