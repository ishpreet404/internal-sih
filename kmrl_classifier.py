"""
Railway document classification module for KMRL and general railway operations.
This module provides functionality to classify documents based on railway-specific keywords
and content patterns.
"""

import re
from typing import Dict, List, Tuple
from collections import defaultdict

class RailwayDocumentClassifier:
    """
    Railway document classifier that categorizes documents based on content analysis
    and keyword matching for railway-specific operations.
    """
    
    def __init__(self):
        """Initialize the classifier with railway-specific categories and keywords."""
        self.railway_categories = {
            'safety_manual': {
                'keywords': [
                    'safety', 'hazard', 'risk', 'emergency', 'accident', 'incident',
                    'emergency response', 'safety protocol', 'hazard identification',
                    'risk assessment', 'safety training', 'accident prevention',
                    'occupational safety', 'personal protective equipment', 'ppe',
                    'emergency evacuation', 'fire safety', 'first aid'
                ],
                'weight': 1.2  # Higher weight for safety-critical content
            },
            'technical_documentation': {
                'keywords': [
                    'specifications', 'technical', 'engineering', 'maintenance', 'repair',
                    'technical specifications', 'engineering drawings', 'maintenance manual',
                    'repair procedures', 'technical standards', 'system specifications',
                    'component specifications', 'installation guide', 'troubleshooting',
                    'calibration', 'testing procedures', 'quality control'
                ],
                'weight': 1.0
            },
            'operational_procedures': {
                'keywords': [
                    'operation', 'procedure', 'protocol', 'guideline', 'instruction',
                    'operating procedures', 'standard operating procedure', 'sop',
                    'operational guidelines', 'work instructions', 'process flow',
                    'operational manual', 'duty instructions', 'shift procedures',
                    'operational safety', 'control procedures'
                ],
                'weight': 1.1
            },
            'schedule_timetable': {
                'keywords': [
                    'schedule', 'timetable', 'departure', 'arrival', 'route',
                    'train schedule', 'service timetable', 'departure time',
                    'arrival time', 'route map', 'frequency', 'service interval',
                    'peak hours', 'off-peak', 'holiday schedule', 'special service'
                ],
                'weight': 0.9
            },
            'compliance_regulatory': {
                'keywords': [
                    'compliance', 'regulation', 'standard', 'requirement', 'audit',
                    'regulatory compliance', 'safety standards', 'industry standards',
                    'compliance audit', 'regulatory requirements', 'certification',
                    'inspection', 'quality assurance', 'standard procedures',
                    'legal requirements', 'regulatory framework'
                ],
                'weight': 1.1
            },
            'training_manual': {
                'keywords': [
                    'training', 'education', 'course', 'certification', 'qualification',
                    'training manual', 'training program', 'educational material',
                    'certification course', 'qualification requirements', 'skill development',
                    'competency', 'learning objectives', 'training schedule',
                    'assessment', 'examination', 'practical training'
                ],
                'weight': 0.8
            },
            'infrastructure': {
                'keywords': [
                    'track', 'signal', 'station', 'platform', 'bridge', 'tunnel',
                    'railway track', 'signaling system', 'station infrastructure',
                    'platform design', 'bridge construction', 'tunnel engineering',
                    'overhead lines', 'power supply', 'track maintenance',
                    'signal maintenance', 'infrastructure development',
                    'civil engineering', 'structural design'
                ],
                'weight': 1.0
            },
            'rolling_stock': {
                'keywords': [
                    'locomotive', 'coach', 'wagon', 'train', 'vehicle',
                    'rolling stock', 'train composition', 'locomotive maintenance',
                    'coach design', 'passenger coach', 'freight wagon',
                    'multiple unit', 'emu', 'dmu', 'electric multiple unit',
                    'diesel multiple unit', 'bogies', 'traction system'
                ],
                'weight': 1.0
            },
            'passenger_services': {
                'keywords': [
                    'passenger', 'ticket', 'booking', 'service', 'customer',
                    'passenger services', 'ticketing system', 'reservation',
                    'customer service', 'passenger amenities', 'accessibility',
                    'passenger information', 'announcements', 'passenger safety',
                    'boarding', 'alighting', 'passenger comfort'
                ],
                'weight': 0.7
            },
            'freight_operations': {
                'keywords': [
                    'freight', 'cargo', 'goods', 'loading', 'unloading',
                    'freight operations', 'cargo handling', 'goods transportation',
                    'loading procedures', 'unloading procedures', 'freight yard',
                    'cargo terminal', 'container handling', 'bulk cargo',
                    'freight scheduling', 'goods wagon'
                ],
                'weight': 0.8
            },
            'signaling_communication': {
                'keywords': [
                    'signaling', 'communication', 'control', 'interlocking', 'block',
                    'signal control', 'communication system', 'train control',
                    'automatic block signaling', 'centralized traffic control',
                    'radio communication', 'data communication', 'control room',
                    'dispatching', 'train detection', 'level crossing'
                ],
                'weight': 1.1
            },
            'electrical_systems': {
                'keywords': [
                    'electrical', 'power', 'traction', 'substation', 'overhead',
                    'electrical system', 'power supply', 'traction power',
                    'electrical substation', 'overhead equipment', 'pantograph',
                    'electrical maintenance', 'power distribution', '25kv',
                    'electrical safety', 'earthing', 'insulation'
                ],
                'weight': 1.0
            }
        }
        
        # KMRL-specific keywords for Kochi Metro
        self.kmrl_keywords = [
            'kmrl', 'kochi metro', 'kerala', 'metro rail', 'rapid transit',
            'kochi', 'ernakulam', 'aluva', 'maharajas college', 'palarivattom',
            'edappally', 'kalamassery', 'cochin', 'metro station'
        ]

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better keyword matching.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        return text

    def calculate_keyword_score(self, text: str, keywords: List[str], weight: float = 1.0) -> float:
        """
        Calculate keyword-based score for a category.
        
        Args:
            text: Text to analyze
            keywords: List of keywords to search for
            weight: Weight multiplier for the category
            
        Returns:
            Calculated score
        """
        text = self.preprocess_text(text)
        
        # Count keyword occurrences
        keyword_count = 0
        total_keywords = len(keywords)
        
        for keyword in keywords:
            keyword = keyword.lower()
            # Check for exact keyword matches and partial matches
            if keyword in text:
                keyword_count += 1
                # Give extra points for multiple occurrences
                keyword_count += text.count(keyword) * 0.1
        
        # Calculate base score
        if total_keywords > 0:
            base_score = keyword_count / total_keywords
        else:
            base_score = 0
        
        # Apply weight and normalization
        weighted_score = base_score * weight
        
        # Normalize to 0-1 range
        normalized_score = min(weighted_score, 1.0)
        
        return normalized_score

    def detect_kmrl_content(self, text: str) -> float:
        """
        Detect KMRL-specific content in the text.
        
        Args:
            text: Text to analyze
            
        Returns:
            KMRL relevance score (0-1)
        """
        text = self.preprocess_text(text)
        
        kmrl_mentions = 0
        for keyword in self.kmrl_keywords:
            if keyword.lower() in text:
                kmrl_mentions += 1
        
        if len(self.kmrl_keywords) > 0:
            return min(kmrl_mentions / len(self.kmrl_keywords) * 2, 1.0)
        return 0.0

    def classify_document(self, text: str, summary: str = "") -> List[Dict[str, any]]:
        """
        Classify a railway document based on its content.
        
        Args:
            text: Main document text
            summary: Optional document summary
            
        Returns:
            List of classification results with categories and confidence scores
        """
        # Combine text and summary
        combined_text = f"{text} {summary}"
        
        if not combined_text.strip():
            return [{
                'category': 'Unknown Document',
                'confidence': 0.1,
                'kmrl_relevance': 0.0
            }]
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, config in self.railway_categories.items():
            score = self.calculate_keyword_score(
                combined_text, 
                config['keywords'], 
                config['weight']
            )
            category_scores[category] = score
        
        # Detect KMRL relevance
        kmrl_score = self.detect_kmrl_content(combined_text)
        
        # Filter categories with meaningful scores
        significant_categories = [
            (category, score) for category, score in category_scores.items() 
            if score > 0.1  # Minimum threshold
        ]
        
        # Sort by score
        significant_categories.sort(key=lambda x: x[1], reverse=True)
        
        # Prepare results
        results = []
        
        if significant_categories:
            for category, score in significant_categories[:5]:  # Top 5 categories
                # Boost score if KMRL content is detected
                if kmrl_score > 0.3:
                    score = min(score * (1 + kmrl_score * 0.5), 1.0)
                
                results.append({
                    'category': self.format_category_name(category),
                    'confidence': round(score, 2),
                    'kmrl_relevance': round(kmrl_score, 2)
                })
        else:
            # Default classification
            base_confidence = 0.3 if kmrl_score > 0.2 else 0.2
            results.append({
                'category': 'General Railway Document',
                'confidence': base_confidence,
                'kmrl_relevance': round(kmrl_score, 2)
            })
        
        return results

    def format_category_name(self, category: str) -> str:
        """
        Format category name for display.
        
        Args:
            category: Category identifier
            
        Returns:
            Formatted category name
        """
        # Replace underscores with spaces and title case
        formatted = category.replace('_', ' ').title()
        
        # Special formatting for specific categories
        replacements = {
            'Sop': 'SOP',
            'Ppe': 'PPE',
            'Emu': 'EMU',
            'Dmu': 'DMU',
            'Kmrl': 'KMRL',
            '25Kv': '25kV'
        }
        
        for old, new in replacements.items():
            formatted = formatted.replace(old, new)
        
        return formatted

    def get_category_insights(self, classifications: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Generate insights based on classification results.
        
        Args:
            classifications: List of classification results
            
        Returns:
            Dictionary containing insights and metadata
        """
        if not classifications:
            return {}
        
        top_category = classifications[0]
        high_confidence_categories = [
            c for c in classifications if c['confidence'] >= 0.7
        ]
        
        insights = {
            'primary_category': top_category['category'],
            'primary_confidence': top_category['confidence'],
            'kmrl_relevance': top_category.get('kmrl_relevance', 0.0),
            'high_confidence_count': len(high_confidence_categories),
            'is_kmrl_document': top_category.get('kmrl_relevance', 0.0) > 0.3,
            'confidence_level': self.get_confidence_description(top_category['confidence']),
            'category_count': len(classifications)
        }
        
        return insights

    def get_confidence_description(self, confidence: float) -> str:
        """
        Get human-readable confidence description.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Confidence description
        """
        if confidence >= 0.9:
            return 'Very High'
        elif confidence >= 0.7:
            return 'High'
        elif confidence >= 0.5:
            return 'Medium'
        elif confidence >= 0.3:
            return 'Low'
        else:
            return 'Very Low'


# Convenience function for direct use
def classify_railway_document(text: str, summary: str = "") -> List[Dict[str, any]]:
    """
    Classify a railway document using the RailwayDocumentClassifier.
    
    Args:
        text: Document text
        summary: Optional document summary
        
    Returns:
        List of classification results
    """
    classifier = RailwayDocumentClassifier()
    return classifier.classify_document(text, summary)


# Example usage and testing
if __name__ == "__main__":
    # Test the classifier
    classifier = RailwayDocumentClassifier()
    
    # Test document
    test_text = """
    Railway Safety Manual for KMRL Operations
    
    This document outlines the safety procedures and protocols for 
    Kochi Metro Rail Limited operations. All staff must follow these
    safety guidelines to ensure safe operation of metro services.
    
    Emergency procedures include evacuation protocols, fire safety
    measures, and accident reporting procedures.
    """
    
    results = classifier.classify_document(test_text)
    insights = classifier.get_category_insights(results)
    
    print("Classification Results:")
    for result in results:
        print(f"- {result['category']}: {result['confidence']:.2f}")
    
    print(f"\nPrimary Category: {insights['primary_category']}")
    print(f"KMRL Relevance: {insights['kmrl_relevance']:.2f}")
    print(f"Is KMRL Document: {insights['is_kmrl_document']}")