"""
Notion integration tools for CrewAI chatbot
"""
import os
from typing import Dict, List, Any, Optional
from notion_client import Client
from pydantic import BaseModel, Field
from crewai_tools import BaseTool


class NotionSearchTool(BaseTool):
    name: str = "notion_search"
    description: str = "Search for pages and databases in Notion workspace"
    
    def __init__(self):
        super().__init__()
        self.notion_token = os.getenv("NOTION_TOKEN")
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        self.notion = Client(auth=self.notion_token)
    
    def _run(self, query: str) -> str:
        """Search Notion for pages and databases containing the query"""
        try:
            results = self.notion.search(query=query, page_size=10)
            
            formatted_results = []
            for item in results.get("results", []):
                title = self._get_title_from_item(item)
                url = item.get("url", "")
                object_type = item.get("object", "")
                
                formatted_results.append({
                    "title": title,
                    "type": object_type,
                    "url": url,
                    "id": item.get("id", "")
                })
            
            return str(formatted_results)
        except Exception as e:
            return f"Error searching Notion: {str(e)}"
    
    def _get_title_from_item(self, item: Dict) -> str:
        """Extract title from Notion item"""
        properties = item.get("properties", {})
        
        # Try to find title property
        for prop_name, prop_value in properties.items():
            if prop_value.get("type") == "title":
                title_array = prop_value.get("title", [])
                if title_array:
                    return title_array[0].get("plain_text", "Untitled")
        
        # Fallback to checking if it's a page with title in different structure
        if "title" in item:
            title_array = item.get("title", [])
            if title_array:
                return title_array[0].get("plain_text", "Untitled")
        
        return "Untitled"


class NotionPageRetrieverTool(BaseTool):
    name: str = "notion_page_retriever"
    description: str = "Retrieve content from a specific Notion page"
    
    def __init__(self):
        super().__init__()
        self.notion_token = os.getenv("NOTION_TOKEN")
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        self.notion = Client(auth=self.notion_token)
    
    def _run(self, page_id: str) -> str:
        """Retrieve content from a Notion page"""
        try:
            # Get page details
            page = self.notion.pages.retrieve(page_id)
            
            # Get page content blocks
            blocks = self.notion.blocks.children.list(page_id)
            
            content = {
                "title": self._get_title_from_item(page),
                "url": page.get("url", ""),
                "last_edited": page.get("last_edited_time", ""),
                "blocks": []
            }
            
            # Process blocks to extract text content
            for block in blocks.get("results", []):
                block_content = self._extract_block_content(block)
                if block_content:
                    content["blocks"].append(block_content)
            
            return str(content)
        except Exception as e:
            return f"Error retrieving Notion page: {str(e)}"
    
    def _get_title_from_item(self, item: Dict) -> str:
        """Extract title from Notion item"""
        properties = item.get("properties", {})
        
        for prop_name, prop_value in properties.items():
            if prop_value.get("type") == "title":
                title_array = prop_value.get("title", [])
                if title_array:
                    return title_array[0].get("plain_text", "Untitled")
        
        return "Untitled"
    
    def _extract_block_content(self, block: Dict) -> Optional[Dict]:
        """Extract content from a Notion block"""
        block_type = block.get("type", "")
        
        if block_type == "paragraph":
            text_content = self._extract_rich_text(block.get("paragraph", {}).get("rich_text", []))
            return {"type": "paragraph", "text": text_content}
        elif block_type == "heading_1":
            text_content = self._extract_rich_text(block.get("heading_1", {}).get("rich_text", []))
            return {"type": "heading_1", "text": text_content}
        elif block_type == "heading_2":
            text_content = self._extract_rich_text(block.get("heading_2", {}).get("rich_text", []))
            return {"type": "heading_2", "text": text_content}
        elif block_type == "heading_3":
            text_content = self._extract_rich_text(block.get("heading_3", {}).get("rich_text", []))
            return {"type": "heading_3", "text": text_content}
        elif block_type == "bulleted_list_item":
            text_content = self._extract_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
            return {"type": "bulleted_list_item", "text": text_content}
        elif block_type == "numbered_list_item":
            text_content = self._extract_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
            return {"type": "numbered_list_item", "text": text_content}
        
        return None
    
    def _extract_rich_text(self, rich_text_array: List[Dict]) -> str:
        """Extract plain text from Notion rich text array"""
        text_parts = []
        for text_item in rich_text_array:
            text_parts.append(text_item.get("plain_text", ""))
        return "".join(text_parts)


class NotionDatabaseQueryTool(BaseTool):
    name: str = "notion_database_query"
    description: str = "Query a Notion database for specific information"
    
    def __init__(self):
        super().__init__()
        self.notion_token = os.getenv("NOTION_TOKEN")
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        self.notion = Client(auth=self.notion_token)
    
    def _run(self, database_id: str, filter_query: str = "") -> str:
        """Query a Notion database"""
        try:
            # Basic query without complex filters for now
            query_params = {"page_size": 20}
            
            results = self.notion.databases.query(database_id, **query_params)
            
            formatted_results = []
            for item in results.get("results", []):
                properties = item.get("properties", {})
                formatted_item = {
                    "id": item.get("id", ""),
                    "url": item.get("url", ""),
                    "last_edited": item.get("last_edited_time", ""),
                    "properties": {}
                }
                
                # Extract property values
                for prop_name, prop_value in properties.items():
                    prop_type = prop_value.get("type", "")
                    
                    if prop_type == "title":
                        title_array = prop_value.get("title", [])
                        if title_array:
                            formatted_item["properties"][prop_name] = title_array[0].get("plain_text", "")
                    elif prop_type == "rich_text":
                        rich_text_array = prop_value.get("rich_text", [])
                        if rich_text_array:
                            formatted_item["properties"][prop_name] = rich_text_array[0].get("plain_text", "")
                    elif prop_type == "select":
                        select_value = prop_value.get("select", {})
                        if select_value:
                            formatted_item["properties"][prop_name] = select_value.get("name", "")
                    elif prop_type == "number":
                        formatted_item["properties"][prop_name] = prop_value.get("number", "")
                    elif prop_type == "date":
                        date_value = prop_value.get("date", {})
                        if date_value:
                            formatted_item["properties"][prop_name] = date_value.get("start", "")
                
                formatted_results.append(formatted_item)
            
            return str(formatted_results)
        except Exception as e:
            return f"Error querying Notion database: {str(e)}"
