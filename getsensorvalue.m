// Compile with $ gcc -o lmutracker lmu.m -framework IOKit -framework CoreFoundation -framework Foundation
// Usage: ./getsensorvalue
// Prints out the value from the ambient light sensor

#include <stdio.h>
#include <string.h>

#import <Foundation/Foundation.h>
#import <IOKit/IOKitLib.h>

io_connect_t dataPort;

enum {
    kGetSensorReadingID   = 0,  // getSensorReading(int *, int *)
    kGetLEDBrightnessID   = 1,  // getLEDBrightness(int, int *)
};

int main (int argc, const char * argv[]) {
    NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
    
    kern_return_t kr = KERN_FAILURE;
    io_service_t serviceObject; 
    
    // Look up a registered IOService object whose class is AppleLMUController  
    serviceObject = IOServiceGetMatchingService(kIOMasterPortDefault,
                                                IOServiceMatching("AppleLMUController"));
    if (serviceObject) {
        kr = IOServiceOpen(serviceObject, mach_task_self(), 0, &dataPort);          
    }   
    IOObjectRelease(serviceObject);
    
    if (kr == KERN_SUCCESS) {
        //Get the ALS reading
        uint32_t scalarOutputCount = 2;
        uint64_t values[scalarOutputCount];
        
        kr = IOConnectCallMethod(dataPort, 
                                    kGetSensorReadingID, 
                                    nil, 
                                    0, 
                                    nil, 
                                    0, 
                                    values, 
                                    &scalarOutputCount, 
                                    nil, 
                                    0);
        
        printf("%llu", MAX(values[0],values[1]));
    }
    
    [pool drain];
    return 0;
}