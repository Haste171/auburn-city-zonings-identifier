# auburn-city-zonings-identifier

Tool for visualizing specific zonings in Auburn, AL

# Example Visualization 

### Zonings that allow 4+ unrelated roomates (highlighted in red) - useful for finding specific housing zones etc.

<p align="center">
  <strong>Before</strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <strong>After</strong>
</p>
<p align="center">
  <img src="data/zoning_map.png" width="45%" />
  <img src="data/preview.png" width="45%" />
</p>



## Command Syntax

```python
python main.py zone-group --image 'data/zoning_map.png' --output 'areas_allowing_4_unrelated.png' --zones MDRD CRD-E CRD-S CRD-U CRD-W CDD NRD RDD UC UN-E UN-S UN-W R --replacement '#0096FF'
```

*This is an example commands to visualize all zonings that are housing/living space zones that allow 4+ unrelated roomates.*

# Data Sources

Auburn Zoning Ordinances - https://www.auburnalabama.org/planning/development-services/zoning-ordinance/

City Zoning Map - https://www.auburnalabama.org/maps/City_Zoning.pdf 
*Converted to png*
