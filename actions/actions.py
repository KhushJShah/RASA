from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

class ValidateOrderPizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_pizza_form"

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        valid_types = ["Veggie", "Protein", "Cheese"]
        if slot_value.capitalize() in valid_types:
            return {"pizza_type": slot_value}
        dispatcher.utter_message(text=f"Sorry, we don't have {slot_value}. Please choose from Veggie, Protein, or Cheese.")
        return {"pizza_type": None}

    d  def validate_topping(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        pizza_type = tracker.get_slot("pizza_type").capitalize()
        valid_toppings = {
            "Veggie": ["onions", "capsicum"],
            "Protein": ["chickpeas", "cottage cheese"],
            "Cheese": ["extra cheese", "oregano"]
        }

        # Split user input into a list of toppings if 'and' exists
        selected_toppings = [t.strip().lower() for t in slot_value.split('and')]

        # Check if all selected toppings are valid for the chosen pizza type
        if all(topping in valid_toppings.get(pizza_type, []) for topping in selected_toppings):
            return {"topping": ", ".join(selected_toppings)}
        
        dispatcher.utter_message(text=f"Sorry, some of those toppings are not available for {pizza_type} pizza.")
        return {"topping": None}

    def validate_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        valid_sizes = ["small", "medium", "large"]
        if slot_value.lower() in valid_sizes:
            return {"size": slot_value}
        
        dispatcher.utter_message(text="Please choose a size from small, medium, or large.")
        return {"size": None}