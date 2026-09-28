// Original source-only WebGPU bridge. Automated package validation: syntax only.
// Vertex storage contract: vec4 position @0, vec4 linear color @16, stride32.
// Uniform: column-major mat4x4<f32>, 64 bytes. No optional features enabled.
const logElement = document.querySelector('#log');
const canvas = document.querySelector('#view');
function log(message) { logElement.textContent += `${message}\n`; logElement.scrollTop = logElement.scrollHeight; }
let running = true;
let device, context, depth;
let slots = [];
let source;
function fail(error) { running = false; log(`STOPPED: ${error?.message ?? error}`); }
const shaderSource = `
struct Vertex { position: vec4<f32>, color: vec4<f32> }
struct Transform { matrix: mat4x4<f32> }
@group(0) @binding(0) var<storage, read> src: array<Vertex>;
@group(0) @binding(1) var<storage, read_write> dst: array<Vertex>;
@group(0) @binding(2) var<uniform> transform: Transform;
@compute @workgroup_size(64)
fn cs_main(@builtin(global_invocation_id) id: vec3<u32>) {
    if (id.x >= arrayLength(&dst)) { return; }
    dst[id.x].position = transform.matrix * src[id.x].position;
    dst[id.x].color = src[id.x].color;
}
`;
const drawSource = `
struct Vertex { position: vec4<f32>, color: vec4<f32> }
@group(0) @binding(0) var<storage, read> vertices: array<Vertex>;
struct Out { @builtin(position) position: vec4<f32>, @location(0) color: vec4<f32> }
@vertex fn vs_main(@builtin(vertex_index) i: u32) -> Out {
    var out: Out; out.position=vertices[i].position; out.color=vertices[i].color; return out;
}
fn srgb(x: vec3<f32>) -> vec3<f32> {
    let v = clamp(x,vec3<f32>(0.0),vec3<f32>(1.0));
    return select(1.055*pow(v,vec3<f32>(1.0/2.4))-0.055,12.92*v,v<=vec3<f32>(0.0031308));
}
@fragment fn fs_main(input: Out) -> @location(0) vec4<f32> {
    // Preferred canvas format is non-sRGB unorm; perform one output encoding here.
    return vec4<f32>(srgb(input.color.rgb),1.0);
}
`;
const identity = () => new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
function multiply(a,b) {
    const out=new Float32Array(16);
    for(let col=0;col<4;col++)for(let row=0;row<4;row++) {
        let sum=0;for(let k=0;k<4;k++)sum+=a[k*4+row]*b[col*4+k];out[col*4+row]=sum;
    }
    return out;
}
function cameraMatrix(seconds,aspect) {
    const s=Math.sin(seconds*.4),c=Math.cos(seconds*.4),m=identity();
    m[0]=c;m[2]=-s;m[8]=s;m[10]=c;m[14]=-3;
    const n=.1,f=20,k=1/Math.tan(Math.PI/6);
    const p=new Float32Array([k/aspect,0,0,0, 0,k,0,0, 0,0,f/(n-f),-1, 0,0,f*n/(n-f),0]);
    return multiply(p,m);
}
function cubeVertices() {
    const v=[[-.6,-.6,-.6],[.6,-.6,-.6],[.6,.6,-.6],[-.6,.6,-.6],[-.6,-.6,.6],[.6,-.6,.6],[.6,.6,.6],[-.6,.6,.6]];
    const faces=[[0,1,2,3],[5,4,7,6],[4,0,3,7],[1,5,6,2],[3,2,6,7],[4,5,1,0]];
    const colors=[[.9,.2,.1],[.1,.7,.9],[.2,.8,.3],[.8,.5,.1],[.6,.2,.8],[.15,.45,.7]];
    const out=[];
    faces.forEach((face,i)=>{for(const k of [0,1,2,0,2,3])out.push(...v[face[k]],1,...colors[i],1);});
    return new Float32Array(out);
}
function upload(data,usage,label) {
    const buffer=device.createBuffer({label,size:data.byteLength,usage:usage|GPUBufferUsage.COPY_DST});
    device.queue.writeBuffer(buffer,0,data);return buffer;
}
async function inspectModule(module,label) {
    const info=await module.getCompilationInfo();
    for(const m of info.messages)log(`${label}: ${m.type} ${m.lineNum}:${m.linePos} ${m.message}`);
    if(info.messages.some(m=>m.type==='error'))throw new Error(`${label} failed compilation`);
}
function encodeCompute(encoder,pipeline,group,count) {
    const pass=encoder.beginComputePass({label:'bounded vertex transform'});
    pass.setPipeline(pipeline);pass.setBindGroup(0,group);pass.dispatchWorkgroups(Math.ceil(count/64));pass.end();
}
function computeGroup(pipeline,src,dst,uniform) {
    return device.createBindGroup({layout:pipeline.getBindGroupLayout(0),entries:[
        {binding:0,resource:{buffer:src}},{binding:1,resource:{buffer:dst}},{binding:2,resource:{buffer:uniform}}]});
}
async function checkReadback(pipeline,count) {
    if(count===0) { log('readback N=0: skipped before resource allocation (PASS policy)');return; }
    const values=new Float32Array(count*8);
    for(let i=0;i<count;i++)values.set([i/128,.25,.5,1,.25,.5,.75,1],i*8);
    const src=upload(values,GPUBufferUsage.STORAGE,'readback source');
    const uniform=upload(identity(),GPUBufferUsage.UNIFORM,'readback identity');
    const dst=device.createBuffer({size:values.byteLength,usage:GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC});
    const read=device.createBuffer({size:values.byteLength,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});
    try {
        const enc=device.createCommandEncoder();encodeCompute(enc,pipeline,computeGroup(pipeline,src,dst,uniform),count);
        enc.copyBufferToBuffer(dst,0,read,0,values.byteLength);device.queue.submit([enc.finish()]);
        await read.mapAsync(GPUMapMode.READ);
        const actual=new Float32Array(read.getMappedRange());
        for(let i=0;i<values.length;i++)if(actual[i]!==values[i])throw new Error(`readback mismatch: N=${count}, float ${i}`);
        read.unmap();log(`readback N=${count}: ${values.length} float components match (PASS)`);
    } finally { await device.queue.onSubmittedWorkDone();for(const b of [src,dst,uniform,read])b.destroy(); }
}
async function start() {
    if(!navigator.gpu)throw new Error('WebGPU unavailable. Use a supported browser/context or the CPU route.');
    const adapter=await navigator.gpu.requestAdapter();
    if(!adapter)throw new Error('No compatible adapter returned.');
    device=await adapter.requestDevice({label:'Package06 device'});
    device.addEventListener('uncapturederror',e=>fail(e.error));
    device.lost.then(info=>{running=false;log(`Device lost/destroyed: ${info.reason}; ${info.message}. Restart page to reinitialize.`);});
    const keys=['maxTextureDimension2D','maxStorageBufferBindingSize','maxComputeWorkgroupSizeX','maxComputeInvocationsPerWorkgroup','minUniformBufferOffsetAlignment'];
    log(`User agent: ${navigator.userAgent}`);
    log(`Enabled features: ${JSON.stringify([...device.features])}`);
    log(`Limits: ${JSON.stringify(Object.fromEntries(keys.map(k=>[k,device.limits[k]])),null,2)}`);
    if(device.limits.maxComputeWorkgroupSizeX<64||device.limits.maxComputeInvocationsPerWorkgroup<64)throw new Error('Required 64-invocation group unsupported.');
    context=canvas.getContext('webgpu');if(!context)throw new Error('Canvas WebGPU context missing.');
    const format=navigator.gpu.getPreferredCanvasFormat();log(`Canvas format: ${format}; explicit output sRGB encoding`);
    device.pushErrorScope('validation');
    const computeModule=device.createShaderModule({label:'transform shader',code:shaderSource});
    const renderModule=device.createShaderModule({label:'draw shader',code:drawSource});
    await inspectModule(computeModule,'compute');await inspectModule(renderModule,'render');
    const compute=await device.createComputePipelineAsync({layout:'auto',compute:{module:computeModule,entryPoint:'cs_main'}});
    const render=await device.createRenderPipelineAsync({layout:'auto',vertex:{module:renderModule,entryPoint:'vs_main'},fragment:{module:renderModule,entryPoint:'fs_main',targets:[{format}]},primitive:{topology:'triangle-list',cullMode:'none'},depthStencil:{format:'depth24plus',depthWriteEnabled:true,depthCompare:'less'}});
    for(const n of [0,1,63,64,65])await checkReadback(compute,n);
    const verts=cubeVertices();source=upload(verts,GPUBufferUsage.STORAGE,'immutable cube source');
    for(let i=0;i<2;i++) {
        const uniform=upload(identity(),GPUBufferUsage.UNIFORM,`frame ${i} matrix`);
        const output=device.createBuffer({label:`frame ${i} transformed`,size:verts.byteLength,usage:GPUBufferUsage.STORAGE});
        slots.push({uniform,output,done:Promise.resolve(),compute:computeGroup(compute,source,output,uniform),render:device.createBindGroup({layout:render.getBindGroupLayout(0),entries:[{binding:0,resource:{buffer:output}}]})});
    }
    const error=await device.popErrorScope();if(error)throw error;
    log('Initialization and bounded readback checks complete. These results apply to THIS browser/device run.');
    let frameIndex=0,lastW=0,lastH=0;
    async function frame(ms) {
        if(!running)return;
        try {
            const rect=canvas.getBoundingClientRect();
            if(rect.width===0||rect.height===0) { requestAnimationFrame(frame);return; }
            const limit=device.limits.maxTextureDimension2D,ratio=window.devicePixelRatio||1;
            const width=Math.max(1,Math.min(limit,Math.floor(rect.width*ratio))),height=Math.max(1,Math.min(limit,Math.floor(rect.height*ratio)));
            if(width!==lastW||height!==lastH) {
                await Promise.all(slots.map(s=>s.done));if(!running)return;
                if(depth)depth.destroy();canvas.width=width;canvas.height=height;
                context.configure({device,format,alphaMode:'opaque'});
                depth=device.createTexture({label:'size-dependent depth',size:[width,height],format:'depth24plus',usage:GPUTextureUsage.RENDER_ATTACHMENT});
                lastW=width;lastH=height;log(`drawable rebuilt: ${width} x ${height}`);
            }
            const slot=slots[frameIndex%slots.length];await slot.done;if(!running)return;
            device.queue.writeBuffer(slot.uniform,0,cameraMatrix(ms/1000,width/height));
            const enc=device.createCommandEncoder({label:`frame ${frameIndex}`});
            encodeCompute(enc,compute,slot.compute,verts.length/8);
            const pass=enc.beginRenderPass({colorAttachments:[{view:context.getCurrentTexture().createView(),clearValue:{r:.025,g:.035,b:.05,a:1},loadOp:'clear',storeOp:'store'}],depthStencilAttachment:{view:depth.createView(),depthClearValue:1,depthLoadOp:'clear',depthStoreOp:'store'}});
            pass.setPipeline(render);pass.setBindGroup(0,slot.render);pass.draw(verts.length/8);pass.end();
            device.queue.submit([enc.finish()]);
            slot.done=device.queue.onSubmittedWorkDone().catch(fail);frameIndex++;
            // Do not await every submitted frame here; wait only when reusing its context.
            if(running)requestAnimationFrame(frame);
        } catch(error){fail(error);}
    }
    if(running)requestAnimationFrame(frame);
}
document.querySelector('#stop').addEventListener('click',async()=>{
    running=false;
    try {
        await initialization;
        if(device)await device.queue.onSubmittedWorkDone();
        for(const s of slots){s.uniform.destroy();s.output.destroy();}
        source?.destroy();depth?.destroy();context?.unconfigure();device?.destroy();log('Stopped; known work completed before resource destruction.');
    }catch(error){log(`Stop diagnostic: ${error.message}`);}
});
const initialization = start().catch(fail);
