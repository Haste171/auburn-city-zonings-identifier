# auburn-city-zonings-identifier

# Example Visualization 

### Zonings that allow 4+ unrelated roomates highlighted in blue () - useful for finding specific housing zones etc.
![Zonings that allow 4+ unrelated roommates](https://i.ibb.co/hFd8qFmq/annotated-city-zoning-ordinances-overlayed.png)

## Command Syntax

```python
python main.py zone-group --image 'data/zoning_map.png' --output 'areas_allowing_4_unrelated.png' --zones MDRD CRD-E CRD-S CRD-U CRD-W CDD NRD RDD UC UN-E UN-S UN-W R --replacement '#0096FF'
```

*This is an example commands to visualize all zonings that are housing/living space zones that allow 4+ unrelated roomates.*

# Data Sources

Auburn Zoning Ordinances - https://www.auburnalabama.org/planning/development-services/zoning-ordinance/

City Zoning Map - https://www.auburnalabama.org/maps/City_Zoning.pdf 
*Converted to png*
