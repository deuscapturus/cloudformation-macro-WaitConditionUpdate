Cloudformation WaitCondition Update Macro
=========================================

The Cloudformation resources AWS::Cloudformation::WaitCondition and AWS::Cloudformation::WaitConditionHandle cannot currently be updated or recreated.  To wait for resource signaling during a *stack update* a new WaitCondition resource needs to be created.  This macro will create new WaitCondition resources based on changes to specified parameters.


Testing
-------

.. code::

  # Unit Test
  python3 -m unittest


Build
-----

.. NOTE::
   S3 Bucket must already exist

Set any required AWS CLI env variables. http://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html

.. code::

  ./build.sh

.. code::

  aws cloudformation package \
    --template deploy-macro.yaml \
    --s3-bucket <YOUR S3 BUCKET> \
    --output-template-file packaged-deploy-macro.yaml

Deploy
------

.. code::

  aws cloudformation deploy \
    --template-file packaged-deploy-macro.yaml \
    --stack-name cloudformation-macro-WaitConditionUpdate \
    --capabilities CAPABILITY_IAM

How to Use
----------

Your template must have contain the parameter `WaitConditionUpdateParameters` and Transform.
When the parameters of WaitConditionUpdateParameters change the logical ids of all WaitCondition resources will be renamed.

.. code:: yaml

   Transform: ['WaitConditionUpdate']
   Parameters:
     WaitConditionUpdateParameters:
       Description: Used by the WaitConditionUpdate transform macro to determine which
         parameter values will be used for naming any WaitCondition resources.  The 
         parameters must only be those which will trigger a recreation of the signaling
         resource when changed.
       Type: CommaDelimitedList
       Default: "PutDefaultsHere"

Example
^^^^^^^

Use a WaitCondition to get a signal when tasks are healthy in a ECS Service

`example-ecs-service.yaml <example-ecs-service.yaml>`_
