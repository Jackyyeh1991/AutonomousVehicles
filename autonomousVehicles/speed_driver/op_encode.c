#include <linux/module.h>
#include <linux/of_device.h>
#include <linux/kernel.h>
#include <linux/gpio/consumer.h>
#include <linux/platform_device.h>
/* YOU WILL NEED OTHER HEADER FILES */
#include <linux/interrupt.h>
#include <linux/gpio.h>

/* YOU WILL HAVE TO DECLARE SOME VARIABLES HERE */
unsigned int irq_number;
struct gpio_desc *speed_encode;
static unsigned int op_count = 0;
module_param(op_count, int, S_IRUGO);

/* ADD THE IN TERRUPT SERVICE ROUTINE HERE */
static irq_handler_t gpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs) {
	// printk("gpio_irq: Interrupt was triggered and ISR was called!\n");
	// if (gpiod_get_value(gpiod_led)) {
	// 	gpiod_set_value(gpiod_led, 0);
	// 	printk("set high");
	// } else {
	// 	gpiod_set_value(gpiod_led, 1);
	// 	printk("set low");
	// }
	op_count += 1;
	return (irq_handler_t) IRQ_HANDLED; 
}


// probe function
static int led_probe(struct platform_device *pd/*INSERT*/)
{
	/*INSERT*/
	printk("op_encode: Loading module... ");
	// struct gpio_desc *__must_check devm_gpiod_get(struct device *dev, const char *con_id, enum gpiod_flags flags)
	speed_encode = devm_gpiod_get(&pd->dev, "userbutton", GPIOD_IN);
	gpiod_set_debounce(speed_encode, 10000000);
	irq_number = gpiod_to_irq(speed_encode);
	request_irq(irq_number, (irq_handler_t) gpio_irq_handler, IRQF_TRIGGER_RISING, "op_encode_driver", NULL);

	return 0;
}

// remove function
static int led_remove(struct platform_device *pd/*INSERT*/)
{
	/* INSERT: Free the irq and print a message */
	free_irq(irq_number, NULL);
	printk("gpiod_driver: irq freed, module removed... ");
	return 0;
}

static struct of_device_id matchy_match[] = {
    // {/*INSERT*/},
	{.compatible = "hello"},
    {/* leave alone - keep this here (end node) */},
};

// platform driver object
static struct platform_driver adam_driver = {
	.probe	 = led_probe/*INSERT*/,
	.remove	 = led_remove/*INSERT*/,
	.driver	 = {
	       .name  = "The Rock: this name doesn't even matter",
	       .owner = THIS_MODULE,
	       .of_match_table = matchy_match/*INSERT*/,
	},
};

module_platform_driver(adam_driver/*INSERT*/);

MODULE_DESCRIPTION("424\'s finest");
MODULE_AUTHOR("GOAT");
MODULE_LICENSE("GPL v2");
MODULE_ALIAS("platform:adam_driver");
