# Principles

The following design sketch tries to follow a few principle ideas:

+ Single Responsibility: Every component is responsible for only one thing.
+ Components ask other components to do something for them, instead of asking
  for information to do it by themselves.
+ The interface to every component should be intuitive to use.

Below, I first wrote down a very "coarse" design description as an overview and
  after that I repeated that overview and added more "fine-grained" information
  on certain parts. At the very bottom you can find explanations for most of
  the terms that are enclosed by quotation marks.


# New Sketch

+ A YAML UI reads user input from a YAML file and passes an object with that
  information to a general UI.

+ The general UI offers the following interface to the YAML UI:
    + A constructor for objects to store user input, defining the expected
      content via it's parameters.
    + A validator that indicates if a user input object's content is complete
      and correct via a boolean value.
    + The validator also returns a list of feedback messages with one message
      for each value that is missing or outside of it's expected range.

+ The YAML UI now proceeds based on whether the user input is fine or not:
    + If the user input is *not* fine, the YAML UI prints the feedback messages
      to the console and terminates the program.
    + Else, if the user input is fine, the YAML UI asks an initializer function
      to initialize the rest of the components, passing the user input object.
      
+ to be continued...


# Coarse Outline

    a "user config file reader" reads in the user config file

    a "user config validator" validates the config's content

    a "config initializer" initializes a config object for each component
    that needs one
          
    all remaining "components" are initialized with their respective config
    object
        initialize the "physics engine"
        initialize the "stem spawner"
            initialize the "stem factory"
            initialize the "forwarder"
        initialize the "reporter"
      
    the stem spawner spawns stems in the physics engine one after the other
    using the stem factory and the forwarder
      
    the reporter writes all desired information on the resulting polter into
    one or more output file(s)
    

# Additional Information

In the beginning, there is just a file path to a user config file.

    a "user config file reader" reads in the user config file
        if any expected information is missing:
            give feedback to the user about what was missing
            abort
    
    a "user config validator" validates the config's content
        if any information is incorrect:
            give feedback to the user about what was expected instead
            abort

Now, there is a complete and correct user config object.

    a "config initializer" initializes a config object for each component that
    needs one
        for each config object:
            set default parameters chosen by us
            overwrite parameters where config information was given by the user
        
Now, there is a complete config object for each component.
        
    all remaining "components" are initialized with their respective config
    object
        initialize the "physics engine"
        initialize the "stem spawner"
            initialize the "stem factory"
            initialize the "forwarder"
        initialize the "reporter"
    
Now, all components are completely initialized.
    
    the stem spawner spawns stems in the physics engine one after the other
    using the stem factory and the forwarder
        
        while the stem factory has stems left:
            the stem factory asks the forwarder for a position
            the stem factory asks the physics engine to create a 3D stem object
            (at the position given by the forwarder), passing the engine a stem
            object that contains all the necessary information (3D and physics
            related)
            
            the stem spawner waits for a certain duration so that the polter
            can settle down
        
Now, all stems have been placed within the simulation.
    
    the reporter writes all desired information on the resulting polter into
    one or more output file(s)
        the reporter asks the stem factory to report on the created stems
        the reporter asks the engine to report on it's general current state
        and also on the individual stems


# Explanations on Individual Components/Keywords
    
*user config file reader*: Trys to open the user config file. Expects to find a
  certain set of inputs in that file. Provides a user config object.
    
*user config validator*: Validates all user config input.

*config initializer*: Provides config objects with default settings for each
  component and overwrites these defaults when given a user config object.
    
*components*: The main "players" in the program flow. Until now these are:
+ user config file reader
+ user config validator
+ config initializer
+ physics engine
+ stem spawer
+ stem factory
+ forwarder
+ reporter
    
*physics engine*: A collection of functions and classes that use the pybullet
  modules to expose physics engine functionality to the other components. By
  doing it this way, we don't need to deal with pybullet outside of this
  self-made engine API.
    
*stem spawner*: An object that contains a stem factory and a forwarder and which
  is responsible for telling these two components to drop new stems at the
  right time, i.e. when the already existing stems have settled after the
  preceding drop.

*stem factory*: An object that produces and stores stem information necessary for
  the engine to spawn new stems.
    
*forwarder*: An object that returns position and orientation information for the
  stem that is to be spawned next, possible based on the current state of the
  simulation.
    
*reporter*: Reports all desired information on the resulting stems and polter.