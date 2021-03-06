=======
Friture
=======

.. image:: https://travis-ci.org/tlecomte/friture.svg?branch=master
    :target: https://travis-ci.org/tlecomte/friture

.. image:: https://ci.appveyor.com/api/projects/status/github/tlecomte/friture?branch=master&svg=true
    :target: https://ci.appveyor.com/project/tlecomte/friture

**Friture** is an application to visualize and analyze live audio data in real-time.

Friture displays audio data in several widgets, such as a scope, a spectrum analyzer, or a rolling 2D spectrogram.

This program can be useful to analyze and equalize the audio response of a hall, or for educational purposes, etc.

The name *Friture* is a french word for *frying*, also used for *noise* in a sound.

See the `project homepage`_ for screenshots and more information.

.. _`project homepage`: http://friture.org

=======
Fork Info
=======
On this Fork I have:

+ Changed the frequencies to notes

  + The scale bars show the notes and C is labeled and clicking displays all note names

    + The frequencies are still acessible by clicking on the plot

  + I can think of very few reasons one would want the actual frequency (except for scientific work)

+ Changed the main window to use `AGeLib`_ for a prettier frame and a more relaxing grey colour that doesn't burn out your eyes

.. _`AGeLib`: https://github.com/AstusRush/AGeLib
