# Craftbeerpi4 Actor Plugin that switched Actor off depending on GPIO input state

## THIS IS AN ALPHA VERSION

- Functions:
	- This Plugin can switch off an actor depending on a GPIO input state

- Parameters:
	- Actor: The Actor that has to be switched off
	- GPIO: The GPIO that s used as input for a high / low signal
	- GPIOstate: High or low. If set to high, the Actor will be siwtched off, when the GPIO turns from low to high. If set to low, it'll work from high to low
	- Notification: If set to Yes, a notification will be sent, when the GPIO triggers the actor
	
- Installation:
	- log in via ssh 
	- clone from the GIT repo
	- source <path to pipx>/pipx/venvs/cbpi4/bin/activate
	- python -m pip install <path to rep>/cbpi4-TimedCycleActor

