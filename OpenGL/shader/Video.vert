#version 130
uniform float	uTime,uDist;		// "Time", from Animate( )
out vec2 vST; // texture coords
out vec3 vN; // normal vector
out vec3 vL; // vector from point to light
out vec3 vE; // vector from point to eye
const vec3 LIGHTPOSITION = vec3( 5., 5., 0. );
const float PI =        3.14159265;
const float AMP =       0.2;
const float W =         2.;

void
main( )
{
	vec4 model = gl_Vertex;
	vST = gl_MultiTexCoord0.st;
	vec4 ECposition = gl_ModelViewMatrix * gl_Vertex;
	vN = normalize( gl_NormalMatrix * gl_Normal ); // normal vector
	vL = LIGHTPOSITION - ECposition.xyz; // vector from the point
	// to the light position
	vE = vec3( 0., 0., 0. ) - ECposition.xyz; // vector from the point
	// to the eye position
	vec3 vert = gl_Vertex.xyz;
	vert.x = model.x+2*abs(sin(1000*uTime*uDist))*fract(sin(dot(vec2(model.y*abs(sin(1000*uTime*uDist)),model.z*abs(sin(1000*uTime*uDist))),vec2(12.9898,78.233)))*43758.5453);
	vert.y = model.y+2*abs(sin(1000*uTime*uDist))*fract(sin(dot(vec2(model.x*abs(sin(1000*uTime*uDist)),model.z*abs(sin(1000*uTime*uDist))),vec2(12.9898,78.233)))*43758.5453);
	vert.z = model.z+2*abs(sin(1000*uTime*uDist))*fract(sin(dot(vec2(model.x*abs(sin(1000*uTime*uDist)),model.y*abs(sin(1000*uTime*uDist))),vec2(12.9898,78.233)))*43758.5453);
	gl_Position = gl_ModelViewProjectionMatrix * vec4( vert, 1. );
}
