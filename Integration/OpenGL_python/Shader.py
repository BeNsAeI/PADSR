from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *

class ShaderProcessor(object):

    def __init__(self):
        pass

    def createAndCompileShader(self, type, source):
        """

        """
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        result = glGetShaderiv(shader, GL_COMPILE_STATUS)

        if (result != 1): # shader didn't compile
            raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
	
        return shader

    def createVertexShader(self):
        """

        """
        return self.createAndCompileShader(GL_VERTEX_SHADER,"""
            #version 130
            uniform sampler2D depth;
            uniform float uMultiplier;
            out vec2 vST; // texture coords
            out vec3 vN; // normal vector
            out vec3 vL; // vector from point to light
            out vec3 vE; // vector from point to eye
            const vec3 LIGHTPOSITION = vec3( 5., 5., 0. );
            const float PI = 3.14159265;
            const float AMP = 0.2;
            const float W = 2.;

            void
            main( )
            {
                vST = gl_MultiTexCoord0.st;
                vec3 vert = gl_Vertex.xyz;
                vert.z = texture2D(depth, vST).r * uMultiplier;
                vec4 ECposition = gl_ModelViewMatrix * gl_Vertex;
                vN = normalize( gl_NormalMatrix * gl_Normal ); // normal vector
                vL = LIGHTPOSITION - ECposition.xyz; // vector from the point
                // to the light position
                vE = vec3( 0., 0., 0. ) - ECposition.xyz; // vector from the point
                // to the eye position
                gl_Position = gl_ModelViewProjectionMatrix * vec4(vert,1);
            }
        """)

    def createFragmentShader(self):
        return self.createAndCompileShader(GL_FRAGMENT_SHADER,"""
            #version 130
            uniform sampler2D RGB;
            uniform float uKa, uKd, uKs; // coefficients of each type of lighting
            uniform float uShininess; // specular exponent
            in vec2 vST; // texture cords
            in vec3 vN; // normal vector
            in vec3 vL; // vector from point to light
            in vec3 vE; // vector from point to eye
            void
            main( )
            {
                vec3 myColor = texture2D(RGB, vST).rgb;
                vec3 Normal = normalize(vN);
                vec3 Light = normalize(vL);
                vec3 Eye = normalize(vE);
                vec3 ambient = uKa * myColor;
                float d = max( dot(Normal,Light), 0. ); // only do diffuse if the light can see the point
                vec3 diffuse = uKd * d * myColor;
                float s = 0.;
                if( dot(Normal,Light) > 0. ) // only do specular if the light can see the point
                {
                    vec3 ref = normalize( reflect( -Light, Normal ) );
                    s = pow( max( dot(Eye,ref),0. ), uShininess );
                }
                vec3 specular = uKs * s * vec3(1,1,1);
                gl_FragColor = vec4( ambient + diffuse + specular, 1. );
            }
            """)