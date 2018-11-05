#version 130
uniform float uKa, uKd, uKs, uTime, uPat; // coefficients of each type of lighting
uniform vec3 uColor; // object color
uniform vec3 uSpecularColor; // light color
uniform float uShininess; // specular exponent
in vec2 vST; // texture cords
in vec3 vN; // normal vector
in vec3 vL; // vector from point to light
in vec3 vE; // vector from point to eye
void
main( )
{
	vec3 myColor = vec3(0,1,1);
	vec3 Normal = normalize(vN);
	vec3 Light = normalize(vL);
	vec3 Eye = normalize(vE);
	if(abs(sin(vST.s*uTime*uPat*100)) > 0.5 && abs(cos(vST.t*uTime*uPat*100)) > 0.5)
	{
		myColor = vec3( 0., 0., 1. );
	}
	vec3 ambient = uKa * myColor;//vec3(0,1,1);//uColor;
	float d = max( dot(Normal,Light), 0. ); // only do diffuse if the light can see the point
	vec3 diffuse = uKd * d * vec3(0,1,1);//uColor;
	float s = 0.;
	if( dot(Normal,Light) > 0. ) // only do specular if the light can see the point
	{
		vec3 ref = normalize( reflect( -Light, Normal ) );
		s = pow( max( dot(Eye,ref),0. ), uShininess );
	}
	vec3 specular = uKs * s * vec3(1,1,1);//uSpecularColor;
	gl_FragColor = vec4( ambient + diffuse + specular, 1. );
}
