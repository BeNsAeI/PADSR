#version 130
//vec2 uV;
//uniform sampler2D depth;
//out vec2 UV2;
void main() {
	vec3 vert;
	vert = gl_Vertex.xyz;
	//vert.z = vert.z + texture(depth, uV).r;
	//UV = uV;
	gl_Position = gl_ModelViewProjectionMatrix * vec4( vert, 1. );
}
