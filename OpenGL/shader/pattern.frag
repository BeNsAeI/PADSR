#version 130
uniform float	uTime;		// "Time", from Animate( )
in vec2		vST;		// texture coords

void
main( )
{
	vec3 myColor = vec3( 0,0,1 );
	if( false )
	{
		myColor = vec3( 0,0,1 );
	}
	gl_FragColor = vec4( myColor,  1. );
}
