import json
import csv
import os
from typing import List, Dict, Any

class DataExporter:
    """
    Export GitHub data to various formats
    """
    
    @staticmethod
    def export_to_json(data: Any, filepath: str) -> bool:
        """
        Export data to JSON file
        
        Args:
            data: Data to export
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Make sure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {str(e)}")
            return False
    
    @staticmethod
    def export_to_csv(data: List[Dict], filepath: str, fields: List[str] = None) -> bool:
        """
        Export list of dictionaries to CSV file
        
        Args:
            data: List of dictionaries to export
            filepath: Output file path
            fields: List of field names to include (if None, use all fields from first item)
            
        Returns:
            True if successful, False otherwise
        """
        if not data:
            print("No data to export")
            return False
            
        try:
            # Make sure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            # Determine fields to include
            if not fields and len(data) > 0:
                # Use all fields from first item
                fields = list(data[0].keys())
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                
                for item in data:
                    # Only include specified fields
                    row = {field: item.get(field, '') for field in fields}
                    writer.writerow(row)
                    
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    @staticmethod
    def export_user_list(users: List[Dict], filepath: str, format: str = 'csv') -> bool:
        """
        Export a list of GitHub users to a file
        
        Args:
            users: List of GitHub user objects
            filepath: Output file path
            format: Output format ('csv' or 'json')
            
        Returns:
            True if successful, False otherwise
        """
        # Extract relevant fields from user objects
        simplified_users = []
        for user in users:
            simplified_users.append({
                'login': user.get('login', ''),
                'name': user.get('name', ''),
                'url': user.get('html_url', ''),
                'type': user.get('type', ''),
                'public_repos': user.get('public_repos', 0),
                'followers': user.get('followers', 0),
                'following': user.get('following', 0),
            })
        
        if format.lower() == 'json':
            return DataExporter.export_to_json(simplified_users, filepath)
        else:  # Default to CSV
            fields = ['login', 'name', 'url', 'type', 'public_repos', 'followers', 'following']
            return DataExporter.export_to_csv(simplified_users, filepath, fields)
    
    @staticmethod
    def export_summary(summary: Dict, filepath: str) -> bool:
        """
        Export a summary report to a file
        
        Args:
            summary: Summary data dictionary
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        # Ensure the filepath has .json extension
        if not filepath.endswith('.json'):
            filepath += '.json'
            
        return DataExporter.export_to_json(summary, filepath) 