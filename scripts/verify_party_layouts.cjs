const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const repo=process.argv[2],html=fs.readFileSync(repo+'/index.html','utf8'),controller=fs.readFileSync(repo+'/affiliation-ui.html','utf8');
const widgets=[...html.matchAll(/<script type="application\/json" data-for="[^"]+"[^>]*>([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]).x).filter(x=>x.nodes&&x.nodes.id.some(id=>String(id).startsWith('POL_')));
assert.equal(widgets.length,3);
const networks={},initial={},data={},keys=['stock','committee','full'],hostIds={stock:'stockView',committee:'committeeView',full:'subcommitteeView'};
const nodeCounts=[400,422,504],edgeCounts=[1292,1383,1618];
const rows=(columns,count)=>Array.from({length:count},(_,i)=>Object.fromEntries(Object.entries(columns).map(([key,value])=>[key,Array.isArray(value)?value[i]:value])));
const colors={Democrat:'#2F6FDB',Republican:'#D64B4B',Stock:'#D6B54A',Committee:'#667A70',Subcommittee:'#A8B7AE'};
let active='stock';
const elements={affiliationLayout:{value:'network'},affiliationLayoutNote:{textContent:''},affiliationClearFocus:{hidden:true}};
for(let i=0;i<widgets.length;i++){
  const key=keys[i],nodes=rows(widgets[i].nodes,nodeCounts[i]),edges=rows(widgets[i].edges,edgeCounts[i]).map((e,index)=>({...e,id:'e'+index}));
  data[key]={nodes,edges};
  initial[key]=Object.fromEntries(nodes.map((node,j)=>[node.id,{x:(j%20)*200,y:Math.floor(j/20)*150}]));
  const positions=structuredClone(initial[key]);
  function dataset(rows){return {get(id){return id===undefined?structuredClone(rows):structuredClone(rows.find(r=>r.id===id));},update(updates){for(const u of updates){Object.assign(rows.find(r=>r.id===u.id),u);if(rows===nodes&&u.x!==undefined)positions[u.id]={x:u.x,y:u.y};}}};}
  elements[hostIds[key]]={clientWidth:1280,clientHeight:720,classList:{contains:()=>active===key},appendChild(){},getBoundingClientRect:()=>({top:0})};
  networks[key]={positions,body:{container:{clientWidth:1280,clientHeight:720},data:{nodes:dataset(nodes),edges:dataset(edges)},nodes:Object.fromEntries(nodes.map(node=>[node.id,{options:{font:{size:11,color:'#30343A'},color:{background:colors[node.group],border:colors[node.group]}}}]))},
    on(){},once(){},setOptions(opts){assert.equal(opts.physics,false);},moveNode(){throw Error('Layout changes must batch coordinates, not redraw once per node');},setSize(){},fit(){},moveTo(opts){assert.ok(Number.isFinite(opts.scale)&&opts.scale>0);},canvasToDOM:({x,y})=>({x:x+640,y:y+360}),unselectAll(){this.selected=[];},stabilize(){throw Error('No restabilization when saved positions exist');}};
}
const immutable=()=>JSON.stringify(Object.fromEntries(keys.map(key=>[key,{nodes:data[key].nodes.map(({id,group,size,title})=>({id,group,size,title})),edges:data[key].edges.map(({id,from,to,width,title,dashes})=>({id,from,to,width,title,dashes}))}])));
const baseline=immutable(),baseColors=Object.fromEntries(keys.map(key=>[key,data[key].edges.map(e=>structuredClone(e.color))]));
const scope={document:{readyState:'complete',getElementById:id=>elements[id],querySelector:()=>null,body:{classList:{contains:()=>true}},createElement(){return {style:{},remove(){}};}},window:{innerWidth:1280,networkInstances:networks,networkInitialPositions:initial,addEventListener(){},updateNetworkShareUrl(){},clearInstitutionFocusForNetwork(){}},setTimeout(){throw Error('No delayed stabilization needed');}};
vm.createContext(scope);vm.runInContext(controller.match(/<script[^>]*>([\s\S]*?)<\/script>/)[1],scope);
function same(actual,expected){assert.equal(JSON.stringify(actual),JSON.stringify(expected));}
elements.affiliationLayout.value='party';elements.affiliationLayout.onchange();
for(const key of keys){
 active=key;assert.equal(scope.window.fitAffiliationNetwork(),true);
 const {nodes,edges}=data[key],n=networks[key];assert.equal(nodes.length,nodeCounts[keys.indexOf(key)]);assert.equal(edges.length,edgeCounts[keys.indexOf(key)]);
 const dems=nodes.filter(node=>node.group==='Democrat'),reps=nodes.filter(node=>node.group==='Republican'),other=nodes.filter(node=>!node.id.startsWith('POL_'));
 assert.ok(Math.max(...dems.map(node=>n.positions[node.id].x))<Math.min(...other.map(node=>n.positions[node.id].x)));
 assert.ok(Math.max(...other.map(node=>n.positions[node.id].x))<Math.min(...reps.map(node=>n.positions[node.id].x)));
 const first=other[0],dx=n.positions[first.id].x-initial[key][first.id].x,dy=n.positions[first.id].y-initial[key][first.id].y*.5;
 for(const node of other){assert.equal(n.positions[node.id].x-initial[key][node.id].x,dx);assert.equal(n.positions[node.id].y-initial[key][node.id].y*.5,dy);}
 assert.equal(new Set(Object.values(n.positions).map(p=>p.x+','+p.y)).size,nodes.length);
 const grouped=structuredClone(n.positions),id='POL_James French Hill',incident=edges.filter(e=>e.from===id||e.to===id),neighbors=new Set([id,...incident.flatMap(e=>[e.from,e.to])]);
 scope.window.highlightAffiliationNode(n,id);
 assert.equal(elements.affiliationClearFocus.hidden,false);
 for(const node of nodes)assert.equal((node.font||n.body.nodes[node.id].options.font).color==='#c4cbd3',!neighbors.has(node.id));
 assert.equal(edges.filter(e=>e.color.color==='rgba(71,85,105,0.8)').length,incident.length);
 elements.affiliationLayout.value='network';elements.affiliationLayout.onchange();same(n.positions,initial[key]);
 for(const node of nodes)assert.equal((node.font||n.body.nodes[node.id].options.font).color==='#c4cbd3',!neighbors.has(node.id));
 scope.window.clearAffiliationFocus(n);assert.equal(elements.affiliationClearFocus.hidden,true);
 for(let j=0;j<edges.length;j++)same(edges[j].color,baseColors[key][j]);
 elements.affiliationLayout.value='party';elements.affiliationLayout.onchange();same(n.positions,grouped);
 n.positions[id]={x:12345,y:67890};scope.window.highlightAffiliationNode(n,id);assert.equal(scope.window.resetAffiliationNetwork(n),true);same(n.positions,grouped);assert.equal(elements.affiliationClearFocus.hidden,true);
 assert.equal(immutable(),baseline);
}
console.log('PASS: all three real datasets; party separation; preserved central geometry; unique positions; exact original-position restoration; direct-neighbor highlighting; focus across layouts; clearing; reset; original edge colors; unchanged node/edge analytical fields.');
