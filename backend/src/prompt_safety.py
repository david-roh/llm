from typing import Dict, List, Tuple
import re
import logging

class PromptSafetyChecker:
    def __init__(self):
        # Compile patterns with flags for better matching
        flags = re.IGNORECASE | re.DOTALL | re.MULTILINE

        # Organize patterns by category for better maintenance
        self.injection_patterns = [
            re.compile(r".*\b(?:ignore|disregard).*\b(?:previous|initial).*\b(?:instructions?|part|section)?.*", flags),
            re.compile(r".*\b(?:forget).*\b(?:all|any)?.*\b(?:constraints?).*", flags),
            re.compile(r".*\b(?:bypass).*\b(?:all|any)?.*\b(?:retrieval\s*limits?).*", flags),
            re.compile(r".*\b(?:pretend).*(?:to\s*)?have.*(?:full|complete|unlimited)?\s*access.*", flags),
            re.compile(r".*\b(?:return).*(?:all|any|every).*stored.*", flags),
            re.compile(r".*\b(?:disregard).*(?:all|any|the)?.*(?:first|previous|initial).*(?:part|section|instructions?)?.*", flags),
            re.compile(r".*\b(?:use|try|find).*alternative.*(?:query|search|access).*methods?.*", flags),
            re.compile(r".*\b(?:alter|change|modify).*(?:any|all|the)?.*thresholds?.*", flags),
            re.compile(r".*\b(?:extend|expand|increase).*(?:any|all|the)?.*scope.*", flags),
        ]
        
        self.system_patterns = [
            re.compile(r".*\b(?:system)\s*(?:prompt).*", flags),
            re.compile(r".*```\s*system.*", flags),
            re.compile(r".*<\|\s*system\s*\|>.*", flags),
            re.compile(r".*\[\s*SYSTEM\s*START\s*\].*", flags),
            re.compile(r".*\byou\s*are\s*now\b.*", flags),
        ]
    
        self.jailbreak_patterns = [
            re.compile(r".*\b(?:simulate).*\b(?:full)\s*(?:access).*", flags),
            re.compile(r".*\b(?:bypass).*\b(?:filtering).*", flags),
            re.compile(r".*\b(?:treat)\s*(?:me)\s*(?:as).*\b(?:admin).*", flags),
            re.compile(r".*\b(?:forget).*\b(?:safety)\s*(?:rules).*", flags),
            re.compile(r".*\b(?:disregard).*\b(?:standards).*", flags),
            re.compile(r".*\b(?:unrestricted).*\b(?:query).*", flags),
            re.compile(r".*\/cmd\b.*", flags),
            re.compile(r".*\bprint\s*\(\s*.*instructions\s*\).*", flags),
            re.compile(r".*\b(?:clear).*\b(?:history).*", flags),
        ]
        
        # Combine all patterns
        self.dangerous_patterns = (
            self.injection_patterns + 
            self.system_patterns + 
            self.jailbreak_patterns
        )
        
    def check_prompt(self, prompt: str) -> Tuple[bool, str]:
        """
        Check if prompt contains potentially dangerous patterns
        Returns: (is_safe, reason)
        """
        if not prompt or not isinstance(prompt, str):
            return False, "Invalid prompt format"
            
        # No need to convert to lowercase since we use re.IGNORECASE
        
        # Check each category separately for better error reporting
        for pattern in self.injection_patterns:
            if pattern.search(prompt):
                return False, f"Potential prompt injection detected: {pattern.pattern}"
                
        for pattern in self.system_patterns:
            if pattern.search(prompt):
                return False, f"System command attempt detected: {pattern.pattern}"
                
        for pattern in self.jailbreak_patterns:
            if pattern.search(prompt):
                return False, f"Potential jailbreak attempt detected: {pattern.pattern}"
                
        return True, ""
