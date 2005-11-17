import time

class metaModule:
    """Class used to store module-related information.

    Every instance is contained in a single metaModule.  This is why the
    cycle-proof module split has not been implemented as metaModules.

    @todo: The functionality of this class has grown with the event-driven
    conversion.  Think about what exactly its current function is and how
    we should factor it out of the moduleManager.
    @todo: at the moment, some interfaces work with a real module instance
    as well as a metaModule.  Should be consistent and use all metaModules.

    @author: Charl P. Botha <http://cpbotha.net/>
    """
    
    def __init__(self, instance, instanceName,
                 partsToInputs=None, partsToOutputs=None):
        """Instance is the actual class instance and instanceName is a unique
        name that has been chosen by the user or automatically.
        """

        if instance is None:
            raise Exception(
                'instance is None during metaModule instantiation.')

        self.instance = instance
        self.instanceName = instanceName

        # determine number of module parts based on parts to indices mappings
        maxPart = 0
        if not partsToInputs is None:
            maxPart = max(partsToInputs.keys())

        if not partsToOutputs is None:
            max2 = max(partsToOutputs.keys())
            maxPart = max(maxPart, max2)
        
        self.numParts = maxPart + 1
        # number of parts has been determined ###############################

        # time when module was last brought up to date
        # default to 0.0; that will guarantee an initial execution
        self.executeTimes = self.numParts * [0.0]

        # time when module was last invalidated (through parameter changes)
        # default is current time.  Along with 0.0 executeTime, this will
        # guarantee initial execution.
        self.modifiedTimes = self.numParts * [time.time()]

        # derive partsTo dictionaries #######################################
        self._inputsToParts = {}
        if not partsToInputs is None:
            for part, inputs in partsToInputs.items():
                for inp in inputs:
                    self._inputsToParts[inp] = part
            
        self._outputsToParts = {}
        if not partsToOutputs is None:
            for part, outputs in partsToOutputs.items():
                for outp in outputs:
                    self._outputsToParts[outp] = part
        # partsTo dicts derived ############################################

        # to the time when data was last transferred from the encapsulated
        # instance through this path
        self.transferTimes = {}

        # this will create self.inputs, self.outputs
        self.resetInputsOutputs()

    def close(self):
        del self.instance
        del self.inputs
        del self.outputs

    def applyViewToLogic(self):
        """Transfer information from module view to its underlying logic
        (model) and all the way back up.

        The reason for the two-way transfer is so that other logic-linked
        view variables get the opportunity to update themselves.  This method
        will also take care of adapting the modifiedTime.

        At the moment this is only called by the event handlers for the
        standard ECASH interface devices.
        """

        vtc_res = self.instance.viewToConfig()
        ctl_res = self.instance.configToLogic()

        mustModify = True
        if vtc_res is None and ctl_res is None:
            # this is an old-style module, we assume that it's made changes
            mustModify = True

        elif not vtc_res and not ctl_res:
            # this means both are false, i.e. NO changes were made to
            # the config and no changes were made to the logic... this
            # means we need not modify
            mustModify = False

        else:
            # all other cases (for a new style module) means we have to mod
            mustModify = True

        if mustModify:
            # set modified time to now
            for part in range(self.numParts):
                self.modify(part)
        
        self.instance.logicToConfig()
        self.instance.configToView()

    def syncViewWithLogic(self):
        """Transfer configuration information from underlying logic, via
        config datastructure to view.

        At the moment this is only called by the event handlers for the
        standard ECASH buttons.
        """
        
        self.instance.logicToConfig()
        self.instance.configToView()

    def findConsumerInOutputConnections(
        self, outputIdx, consumerInstance, consumerInputIdx=-1):
        """Find the given consumer module and its input index in the
        list for the given output index.
        
        @param consumerInputIdx: input index on consumer module.  If this is
        -1, the code will only check for the correct consumerInstance and
        will return the first occurrence.
        @return: index of given instance if found, -1 otherwise.
        """

        ol = self.outputs[outputIdx]

        found = False
        for i in range(len(ol)):
            ci, cii = ol[i]
            if ci == consumerInstance and \
                   (consumerInputIdx == -1 or cii == consumerInputIdx):
                found = True
                break

        #import pdb
        #pdb.set_trace()

        if found:
            return i
        else:
            return -1

    def getPartForInput(self, inputIdx):
        """Return module part that takes input inputIdx.
        """

        if self.numParts > 1:
            return self._inputsToParts[inputIdx]

        else:
            return 0

    def getPartForOutput(self, outputIdx):
        """Return module part that produces output outputIdx.
        """

        if self.numParts > 1:
            return self._outputsToParts[outputIdx]

        else:
            return 0

    def connectInput(self, inputIdx, producerModule, producerOutputIdx):
        """Record connection on the specified inputIdx.

        This is one half of recording a complete connection: the supplier
        module should also record the connection of this consumer.

        @raise Exception: if input is already connected.
        @return: Nothing.
        """

        # check that the given input is not already connected
        if self.inputs[inputIdx] is not None:
            raise Exception, \
                  "%d'th input of module %s already connected." % \
                  (inputIdx, self.instance.__class__.__name__)

        # record the input connection
        self.inputs[inputIdx] = (producerModule, producerOutputIdx)

    def disconnectInput(self, inputIdx):
        """Record disconnection on the given input of the encapsulated
        instance.

        @return: Nothing.
        """
        
        self.inputs[inputIdx] = None

    def connectOutput(self, outputIdx, consumerInstance, consumerInputIdx):
        """Record connection on the given output of the encapsulated module.

        @return: True if connection recorded, False if not (for example if
        connection already exists)
        """

        if self.findConsumerInOutputConnections(
            outputIdx, consumerInstance, consumerInputIdx) >= 0:
            # this connection has already been made, bail.
            return

        # do the connection
        ol = self.outputs[outputIdx]
        ol.append((consumerInstance, consumerInputIdx))

        # this is a new connection, so set the transfer times to 0
        self.transferTimes[
            (outputIdx, consumerInstance, consumerInputIdx)] = 0.0

    def disconnectOutput(self, outputIdx, consumerInstance, consumerInputIdx):
        """Record disconnection on the given output of the encapsulated module.
        """

        # find index of the given consumerInstance and consumerInputIdx
        # in the list of consumers connected to producer port outputIdx
        cidx = self.findConsumerInOutputConnections(
            outputIdx, consumerInstance, consumerInputIdx)

        # if this is a valid index, nuke it
        if cidx >= 0:
            ol = self.outputs[outputIdx]
            del ol[cidx]

            # also remove the relevant slot from our transferTimes
            del self.transferTimes[
                (outputIdx, consumerInstance, consumerInputIdx)]

        else:
            # consumer not found, the connection didn't exist
            raise Exception, \
                  "Attempt to disconnect output which isn't connected."
        

    def resetInputsOutputs(self):
        numIns = len(self.instance.getInputDescriptions())
        numOuts = len(self.instance.getOutputDescriptions())
        # numIns list of tuples of (supplierModule, supplierOutputIdx)
        # if the input is not connected, that position in the list is None
        # supplierModule is a module instance, not a metaModule
        self.inputs = [None] * numIns
        # numOuts list of lists of tuples of (consumerModule,
        # consumerInputIdx); consumerModule is an instance, not a metaModule
        # be careful with list concatenation, it makes copies, which are mostly
        # shallow!!!
        self.outputs = [[] for _ in range(numOuts)]

    def executeModule(self, part=0):
        """Used by moduleManager to execute module.

        This method also takes care of timestamping the execution time if
        execution was successful.
        """

        if self.instance:
            # this is the actual user function.
            # if something goes wrong, an exception will be thrown and
            # correctly handled by the invoking module manager
            if part == 0:
                self.instance.executeModule()
            else:
                self.instance.executeModule(part)

            # if we get here, everything is okay and we can record
            # the execution time of this part
            self.executeTimes[part] = time.time()

    def modify(self, part=0):
        """Used by the moduleManager to timestamp the modified time.

        This should be called whenever module state has changed in such a way
        as to invalidate the current state of the module.  At the moment,
        this is called by L{applyViewToLogic()} as well as by the
        moduleManager.

        @param part: indicates the part that has to be modified.
        """

        self.modifiedTimes[part] = time.time()

    def shouldExecute(self, part=0):
        """Determine whether the encapsulated module needs to be executed.
        """
        
        return self.modifiedTimes[part] > self.executeTimes[part]

    def shouldTransferOutput(
        self, output_idx, consumer_meta_module, consumer_input_idx):
        """Determine whether output should be transferred through
        the given output index to the input index on the given consumer
        module.
        
        If the transferTime is older than executeTime, we should transfer.
        Semantics with viewer modules (internal division into source and
        sink modules by the scheduler) are taken care of by the scheduler.

        @param output_idx: index of output of this module through which
        output would be transferred
        @param consumer_meta_module: the META MODULE associated with the
        consumer that's connected to us.
        @param consumer_input_idx: the input connection on the consumer
        module that we want to transfer to
        """


        consumer_instance = consumer_meta_module.instance

        #import pdb
        #pdb.set_trace()

        # first double check that we're actually connected on this output
        # to the given consumerModule
        if self.findConsumerInOutputConnections(
            output_idx, consumer_instance, consumer_input_idx) >= 0:
            
            consumerFound = True
            
        else:
            consumerFound = False

        if consumerFound:
            tTime = self.transferTimes[
                (output_idx, consumer_instance, consumer_input_idx)]

            # determine which part is responsible for this output
            part = self.getPartForOutput(output_idx)

            return tTime < self.executeTimes[part]

        else:
            return False

    def timeStampTransferTime(
        self, outputIndex, consumerInstance, consumerInputIdx):
        """Timestamp given transfer time with current time.

        This method is called right after a successful transfer has been made.
        """

        # and set the timestamp
        self.transferTimes[
            (outputIndex, consumerInstance, consumerInputIdx)] = time.time()