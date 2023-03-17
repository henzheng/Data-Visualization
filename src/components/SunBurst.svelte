<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";

    onMount(async () => {
        const height: number = 700;
        const width: number = 960;
        const radius: number = (Math.min(width, height) / 2) - 10;

        let formatNumber = d3.format(",d");

        const xScale = d3.scaleLinear().range([0, 2* Math.PI]);
        const yScale = d3.scaleSqrt().range([0, radius]);

        interface PokemonNode {
            id: number;
            name: string;
            size: number;
            api_url: string;
            front_sprite_url: string;
            abilities: string[];
            stats: [
                {
                    base_stat: number;
                    effort: number;
                    stat: {
                        name: string;
                        url: string;
                    }
                }
            ];
            total_base_stats: number;
        }

        interface TypeNode {
            name: string,
            children: PokemonNode[]
        }

        interface Data {
            name: string;
            children: TypeNode[];
        }

        const color = d3.scaleOrdinal(d3.schemeTableau10);
        const partition = d3.partition<Data>().size([2 * Math.PI, radius]);

        const arc: any = d3.arc()
            .startAngle((d: any) => Math.max(0, Math.min(2 * Math.PI, xScale(d.x))))
            .endAngle((d: any) => Math.max(0, Math.min(2 * Math.PI, xScale(d.x + d.dx))))
            .innerRadius((d: any) => Math.max(0, yScale(d.y)))
            .outerRadius((d: any) => Math.max(0, yScale(d.y + d.dy)));
            const svg = d3.select("body")
    
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 +  "," + (height / 2) + ")");
    
            const data = d3.hierarchy<Data>(await d3.json<Data>("/PokemonFlare.json"));
            
            svg.selectAll<SVGPathElement, any>("path")
            .data(partition(data).descendants() as any)
            .join("path")
            .attr("d", arc)
            .style("fill", (d: any) => color((d.data.children ? d : d.parent).data.name))
            .on("click", click)
            .append("title")
            .text((d: any) => `${(d.data as PokemonNode).name}\n${formatNumber((d.data as PokemonNode).size)}`);

            svg.selectAll("path")
            .data(partition(data).descendants())
            .enter()
            .append("path")
            .attr("d", arc)
            .style("fill", (d) => color((d.children ? d : d.parent).name))
            .on("click", click)
            .append("title")
            .text((d) => d.name + "\n" + formatNumber(d.value)) 

            function click(d: any) {
                svg.transition()
                    .duration(750)
                    .tween("scale", function() {
                        var xd = d3.interpolate(xScale.domain(), [d.x, d.x + d.dx]),
                            yd = d3.interpolate(yScale.domain(), [d.y, 1]),
                            yr = d3.interpolate(yScale.range(), [d.y ? 20 : 0, radius]);
                        return (t) => { 
                            xScale.domain(xd(t)); yScale.domain(yd(t)).range(yr(t)); 
                        };
                    })
                    .selectAll("path")
                    .attrTween("d", (d: any) => () => arc(d));

            }
            d3.select(self.frameElement).style("height", height + "px");
        });
</script>
