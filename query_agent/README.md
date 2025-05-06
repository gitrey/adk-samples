# Query Agent

### All queries:
```
queries = [
            ("1", "Describe this image in detail."),
            ("2", "What is the main subject of this image?"),
            ("3", "List the colors present in this image."),
            ("4", "What emotions does this image convey?"),
            ("5", "Identify any objects or people in this image."),
            ("6", "What is the setting of this image?"),
            ("7", "Describe the lighting in this image."),
            ("8", "What is the mood of this image?"),
            ("9", "What story does this image tell?"),
            ("10", "What is the significance of this image?"),
            ("11", "What is the historical context of this image?"),
            ("12", "What techniques were used to create this image?"),
            ("13", "What is the intended audience for this image?"),
            ("14", "What is the message of this image?"),
            ("15", "How does this image relate to current events?"),
            ("16", "What is the cultural significance of this image?"),
            ("17", "What is the artistic style of this image?"),
            ("18", "What is the purpose of this image?"),
            ("19", "What is the composition of this image?"),
            ("20", "What is the perspective of this image?"),
        ]
```

### Run agent:
```python
python3 query_agent/agent.py
```

### Prompt:
```
I'm interested in emotions and mood.
```

### Output:
```
```json
{
  "queries": [
    {
      "query_id": "4",
      "description": "What emotions does this image convey?"
    },
    {
      "query_id": "8",
      "description": "What is the mood of this image?"
    }
  ]
}
```


### Prompt:
```
I'm interested in the artistic style
```

### Output:
```
```json
{
  "relevant_queries": [
    {
      "query_id": "17",
      "description": "What is the artistic style of this image?"
    },
    {
      "query_id": "12",
      "description": "What techniques were used to create this image?"
    }
  ]
}
```